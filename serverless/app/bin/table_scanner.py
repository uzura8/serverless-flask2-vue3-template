import argparse
from app.models.dynamodb import Field, SiteConfig
from pprint import pprint

class TableScanner:
    def __init__(self):
        self.allowed_tables = ['field', 'post', 'site_config']

    def __del__(self):
        pass

    def main(self, table, operation):

        if table not in self.allowed_tables:
            print(f"Error: Invalid table name '{table}'.")
            return

        # Generate class name from table name as PasscalCase
        class_name = ''.join(word.capitalize() for word in table.split('_'))

        # Get class object from class name using globals()
        model_class = globals()[class_name]

        if operation == 'scan':
            items = model_class.scan()
            pprint(items)
        elif operation == 'delete' or operation == 'truncate':
            model_class.truncate()
            print(f'{class_name}.delete() executed.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('table', choices=['field', 'post'], help="Choose the table: 'field' or 'post'")
    parser.add_argument('operation', choices=['scan', 'delete', 'truncate'], help="Choose the operation: 'scan' or 'delete'")
    args = parser.parse_args()

    scanner = TableScanner()
    scanner.main(args.table, args.operation)
