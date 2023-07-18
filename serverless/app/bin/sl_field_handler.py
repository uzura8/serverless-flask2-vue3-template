import argparse
from app.models.dynamodb import Field
import csv
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)


# 現在のスクリプトの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSVの相対パスを指定
CSV_FILE_REL_PATH = '../../develop/var/sl_field.csv'

# 絶対パスを計算
abs_path_to_csv = os.path.join(current_dir, CSV_FILE_REL_PATH)
CSV_FILE_PATH = os.path.normpath(abs_path_to_csv)


class SlFieldHandler:
    def __init__(self, csv_file_path):
        print('== START ==')
        self.csv_file_path = csv_file_path
        self.csvfile = None
        self.reader = None
        self.fieldnames = ['fieldId', 'name',
                           'fieldType', 'address', 'website']

    def __del__(self):
        self.csvfile.close()
        print('== END ==')

    def load_csv(self):
        self.csvfile = open(self.csv_file_path, 'r', encoding='utf-8-sig')
        self.reader = csv.DictReader(self.csvfile)
        for row in self.reader:
            self.save_fields(row)

    def write_to_csv(self):
        data_to_write = Field.scan()  # Get data from Field.scan()
        formatted_data = []
        for item in data_to_write:
            # Extract only needed fields
            formatted_data.append({key: item[key] for key in self.fieldnames})
        self.csvfile = open(self.csv_file_path, 'w',
                            newline='', encoding='utf-8-sig')
        writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        writer.writeheader()
        writer.writerows(formatted_data)

    def save_fields(self, vals):
        field = None
        field_id = vals.get('fieldId')
        query_key = {'p': {'key': 'fieldId', 'val': field_id}}
        if field_id:
            field = Field.get_one(query_key)
            if field and vals != field:
                del vals['fieldId']
                Field.update(query_key, vals, True)
        else:
            Field.create(vals, 'fieldId')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=[
                        'load', 'write'], help='operation to perform')
    args = parser.parse_args()
    handler = SlFieldHandler(CSV_FILE_PATH)
    if args.operation == 'load':
        handler.load_csv()
    elif args.operation == 'write':
        handler.write_to_csv()
