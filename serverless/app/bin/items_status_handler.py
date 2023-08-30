from app.models.dynamodb import Server, Repository, Job
from app.utils.date import utc_iso
import os
import sys
import argparse
from pprint import pprint
import boto3


parent_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

allowed_tables = ['server', 'repository', 'job']


class ItemsStatusHandler:
    def __init__(self):
        self.ddb_client = boto3.client('dynamodb')
        self.allowed_tables = allowed_tables

    def __del__(self):
        pass

    def main(self, table, uid, status):

        if table not in self.allowed_tables:
            print(f"Error: Invalid table name '{table}'.")
            return

        # Generate class name from table name as PasscalCase
        class_name = ''.join(word.capitalize() for word in table.split('_'))
        # Get class object from class name using globals()
        self.model_class = globals()[class_name]

        if table == 'server':
            uid_name = 'domain'
            if status not in ['0', '1']:
                print(f"Error: Invalid status '{status}'.")
                return

            item = self.model_class.get_one({uid_name: uid})
            if not item:
                raise Exception(f"Error: Invalid repoId '{uid}'.")

            vals = {'isExecuting': status}
            self.update_item(uid_name, uid, vals)

        elif table == 'repository':
            uid_name = 'repoId'
            if status not in ['pending', 'inProgress', 'completed', 'failed']:
                print(f"Error: Invalid status '{status}'.")
                return

            if uid == 'all':
                items = self.model_class.scan()
                for item in items:
                    self.update_repo(uid_name, item[uid_name], status)
            else:
                item = self.model_class.get_one({uid_name: uid})
                if not item:
                    raise Exception(f"Error: Invalid repoId '{uid}'.")
                self.update_repo(uid_name, uid, status)

        elif table == 'job':
            uid_name = 'jobId'
            if status not in ['pending', 'inProgress', 'completed', 'failed']:
                print(f"Error: Invalid status '{status}'.")
                return

            if uid == 'all':
                items = self.model_class.scan()
                for item in items:
                    self.update_job(uid_name, item[uid_name], status, item['createdAt'])
            else:
                item = self.model_class.get_one({uid_name: uid})
                if not item:
                    raise Exception(f"Error: Invalid jobId '{uid}'.")
                self.update_job(uid_name, uid, status, item['createdAt'])


    def update_repo(self, uid_name, uid, status):
        upd_datetime = utc_iso()
        vals = {
            'deployStatus': status,
            'deployStatusUpdatedAt': '#'.join([status, upd_datetime]),
        }
        self.update_item(uid_name, uid, vals)


    def update_job(self, uid_name, uid, status, created_at):
        vals = {
            'deployStatus': status,
            'deployStatusCreatedAt': '#'.join([status, created_at]),
        }
        self.update_item(uid_name, uid, vals)

    def update_item(self, uid_name, uid, vals):
        res = self.model_class.update({uid_name: uid}, vals)
        pprint(res)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('table', choices=allowed_tables)
    parser.add_argument('uid')
    parser.add_argument('status')
    args = parser.parse_args()

    handler = ItemsStatusHandler()
    handler.main(args.table, args.uid, args.status)
