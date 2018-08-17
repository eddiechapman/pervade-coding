import os
import csv

CONFIG_PATH = os.path.split(__file__)[0]
INFILE = os.path.join(CONFIG_PATH, '180806-db-update-awards.csv')
OUTFILE = os.path.join(CONFIG_PATH, '180806-db-update-awards-out.csv')


def replace_linebreaks(reader):
    modified_csv = []
    for row in reader:
        row[7] = row[7].replace('<br/>', '\n')
        modified_csv.append(row)
    return modified_csv


def write_csv(OUTFILE, modified_csv):
    with open(OUTFILE, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(modified_csv)


if __name__ == '__main__':
    with open(INFILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        modified_csv = replace_linebreaks(reader)
        write_csv(OUTFILE, modified_csv)