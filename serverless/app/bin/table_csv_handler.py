import argparse
import csv
import os
import sys
from app.models.dynamodb import Category, Field, Maker, Gun
from app.utils.dict import conv_flat_dict_to_nested, flatten_dict
from app.utils.string import to_pascal_case
# from pprint import pprint

parent_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

CSV_DIR_REL_PATH = '../../develop/var/'
TARGET_TABLES = [
    {
        'name': 'category',
        'pkey': 'cateId',
        'attrs': ['contentDiv', 'cateId', 'parentId', 'parentPath', 'orderNo',
                  'slug', 'labels.en', 'labels.ja', 'contentDivSlug'],
        'int_attrs': ['cateId', 'orderNo', 'parentId'],
    },
    {
        'name': 'field',
        'pkey': 'fieldId',
        'attrs': ['fieldId', 'name', 'fieldType', 'address', 'website'],
        'int_attrs': [],
    },
    {
        'name': 'maker',
        'pkey': 'makerId',
        'attrs': ['makerId', 'slug', 'labels.ja', 'labels.en', 'categoryRegionSlug', 'website', 'description'],
        'int_attrs': [],
    },
    {
        'name': 'gun',
        'pkey': 'gunId',
        'attrs': ['gunId', 'labels.ja', 'labels.en', 'makerId', 'gunType', 'poweredType', 'asin'],
        'int_attrs': [],
    },
]
ALLOWED_TABLES = [table['name'] for table in TARGET_TABLES]


class TableCsvHandler:
    def __init__(self, table_name, pkey_name=''):
        print('== START ==')

        results = [t for t in TARGET_TABLES if t['name'] == table_name]
        if not results:
            print(f"Error: Invalid table name '{table_name}'.")
            return

        self.table_info = results[0]
        self.model = globals()[to_pascal_case(table_name)]
        self.csv_file_path = self.get_file_path(table_name, CSV_DIR_REL_PATH)
        self.csv_file = None
        self.reader = None
        self.pkey_name = pkey_name if pkey_name else f'{table_name}Id'
        self.int_attrs = []

    def __del__(self):
        self.csv_file.close()
        print('== END ==')

    def load_csv(self):
        self.csv_file = open(self.csv_file_path, 'r', encoding='utf-8-sig')
        self.reader = csv.DictReader(self.csv_file)
        for row in self.reader:
            row = {k: v for k, v in row.items() if k.strip()}
            self.save(row)

    def write_to_csv(self):
        field_names = self.table_info['attrs']
        data_to_write = self.model.scan()
        formatted_data = []
        for item in data_to_write:
            formatted_item = flatten_dict(item)
            formatted_data.append(
                {key: formatted_item[key] for key in field_names})
        self.csv_file = open(self.csv_file_path, 'w',
                             newline='', encoding='utf-8-sig')
        writer = csv.DictWriter(self.csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(formatted_data)

    def save(self, vals):
        item = None
        for attr in self.table_info['int_attrs']:
            vals[attr] = int(vals[attr])
        vals = conv_flat_dict_to_nested(vals)
        pkey_value = vals.get(self.pkey_name)
        query_key = {self.pkey_name: pkey_value}
        if pkey_value:
            item = self.model.get_one(query_key)
            if not item:
                self.model.create(vals, self.pkey_name)
            elif vals != item:
                del vals[self.pkey_name]
                self.model.update(query_key, vals, True)
        else:
            self.model.create(vals, self.pkey_name)

    @staticmethod
    def get_file_path(table_name, rel_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        rel_path = f'{rel_path}sl_{table_name}.csv'
        abs_path = os.path.join(current_dir, rel_path)
        return os.path.normpath(abs_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('table', choices=ALLOWED_TABLES,
                        help="Choose the table: 'field' or 'post'")
    parser.add_argument('operation', choices=[
                        'load', 'write'], help='Choose the operation')
    args = parser.parse_args()
    handler = TableCsvHandler(args.table)
    if args.operation == 'load':
        handler.load_csv()
    elif args.operation == 'write':
        handler.write_to_csv()
