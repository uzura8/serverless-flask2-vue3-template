import argparse
import csv
import os
import sys
from app.models.dynamodb import Category
from app.utils.dict import conv_flat_dict_to_nested
# from pprint import pprint

parent_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)


# 現在のスクリプトの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSVの相対パスを指定
CSV_FILE_REL_PATH = '../../develop/var/sl_category.csv'

# 絶対パスを計算
abs_path_to_csv = os.path.join(current_dir, CSV_FILE_REL_PATH)
CSV_FILE_PATH = os.path.normpath(abs_path_to_csv)


class SlCategoryHandler:
    def __init__(self, csv_file_path):
        print('== START ==')
        self.csv_file_path = csv_file_path
        self.csvfile = None
        self.reader = None
        self.fieldnames = ['contentDiv', 'cateId', 'parentId', 'parentPath', 'orderNo',
                           'slug', 'label_en', 'label_ja', 'parentPathOrderNo', 'contentDivSlug']
        self.pkey_name = 'cateId'
        self.int_attrs = ['cateId', 'orderNo', 'parentId']

    def __del__(self):
        self.csvfile.close()
        print('== END ==')

    def load_csv(self):
        self.csvfile = open(self.csv_file_path, 'r', encoding='utf-8-sig')
        self.reader = csv.DictReader(self.csvfile)
        for row in self.reader:
            row = {k: v for k, v in row.items() if k.strip()}
            self.save(row)

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

    def save(self, vals):
        item = None
        for attr in self.int_attrs:
            vals[attr] = int(vals[attr])
        vals = conv_flat_dict_to_nested(vals)
        pkey_value = vals.get(self.pkey_name)
        query_key = {self.pkey_name: pkey_value}
        if pkey_value:
            item = Category.get_one(query_key)
            if not item:
                Category.create(vals)
            elif vals != item:
                del vals[self.pkey_name]
                Category.update(query_key, vals, True)
        else:
            Category.create(vals)

    def hoge(original_dict):
        new_dict = {}
        for k, v in original_dict.items():
            parts = k.split('.')
            if len(parts) > 1:
                if parts[0] not in new_dict:
                    new_dict[parts[0]] = {}
                new_dict[parts[0]][parts[1]] = v
            else:
                new_dict[k] = v
        return new_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=[
                        'load', 'write'], help='operation to perform')
    args = parser.parse_args()
    handler = SlCategoryHandler(CSV_FILE_PATH)
    if args.operation == 'load':
        handler.load_csv()
    elif args.operation == 'write':
        handler.write_to_csv()
