import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

import csv
from app.models.dynamodb import Field

# 現在のスクリプトの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSVの相対パスを指定
CSV_FILE_REL_PATH = '../../develop/var/sl_field.csv'

# 絶対パスを計算
abs_path_to_csv = os.path.join(current_dir, CSV_FILE_REL_PATH)
CSV_FILE_PATH = os.path.normpath(abs_path_to_csv)

class SlFieldImporter:
    def __init__(self, csv_file_path):
        print('== START ==')
        self.csv_file_path = csv_file_path
        self.csvfile = None
        self.reader = None


    def __del__(self):
        self.csvfile.close()
        print('== END ==')


    def load_csv(self):
        self.csvfile = open(self.csv_file_path, 'r', encoding='utf-8-sig')
        self.reader = csv.DictReader(self.csvfile)


    def main(self):
        #items = Field.scan()
        self.load_csv()
        for row in self.reader:
            self.create_field(row)


    def create_field(self, vals):
        Field.create(vals, 'fieldId')

if __name__ == '__main__':
    importer = SlFieldImporter(CSV_FILE_PATH)
    importer.main()
