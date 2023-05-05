import csv
from app.models.dynamodb import Field

CSV_FILE_PATH = '../develop/var/sl_field.csv'

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
        self.csvfile = open(self.csv_file_path, 'r', encoding='utf-8')
        self.reader = csv.DictReader(self.csvfile)


    def main(self):
        items = Field.scan()
        self.load_csv()
        for row in self.reader:
            self.create_field(row)


    def create_field(self, vals):
        Field.create(vals, 'fieldId')

if __name__ == '__main__':
    importer = SlFieldImporter(CSV_FILE_PATH)
    importer.main()
