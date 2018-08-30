import os
import csv

CONFIG_PATH = os.path.split(__file__)[0]
INFILE = os.path.join(CONFIG_PATH, 'NSF_Funded_Pis_CISE.csv')
OUTFILE = os.path.join(CONFIG_PATH, 'NSF_Funded_Pis_CISE-deduped.csv')
ERROR_FILE = os.path.join(CONFIG_PATH, 'NSF_Funded_Pis_CISE-duplicates.csv')


def validate_abstract(row):
    row[6] = row[6].replace('<br/>', '<br>')
    row[6] = row[6].replace('&#8203', '')
    row[6] = row[6].lstrip()
    row[6] = row[6].rstrip()
    return row


def validate_character_length(row, i):
    if len(row[0]) > 300:
        print('ERROR: invalid character length. Row #' + str(i), ', column #0, length:' + str(len(row[0])), '(max 300')
    if len(row[1]) > 1000:
        print('ERROR: invalid character length. Row #' + str(i), ', column #1, length:' + str(len(row[1])), '(max 1000')
    if len(row[2]) > 128:
        print('ERROR: invalid character length. Row #' + str(i), ', column #2, length:' + str(len(row[2])), '(max 128')
    if len(row[3]) > 1000:
        print('ERROR: invalid character length. Row #' + str(i), ', column #3, length:' + str(len(row[3])), '(max 1000')
    if len(row[4]) > 1000:
        print('ERROR: invalid character length. Row #' + str(i), ', column #4, length:' + str(len(row[4])), '(max 1000')
    if len(row[5]) > 1000:
        print('ERROR: invalid character length. Row #' + str(i), ', column #5, length:' + str(len(row[5])), '(max 1000')


def validate_type(row, i):
    if isinstance(row[0], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[0])), '(Intended str)')
    if isinstance(row[1], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[1])), '(Intended str)')
    if isinstance(row[2], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[2])), '(Intended str)')
    if isinstance(row[3], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[3])), '(Intended str)')
    if isinstance(row[4], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[4])), '(Intended str)')
    if isinstance(row[5], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[5])), '(Intended str)')
    if isinstance(row[6], str) == False:
        print('ERROR: invalid input type. Row #' + str(i), ', column #, type:' + str(type(row[6])), '(Intended str)')
    for char in row[7]:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print('ERROR: invalid input type. Row #' + str(i), ', column #, bad character:' + char, '(Intended int)')


def validate_award_id(row, award_ids, i):
    remove_dupes = False
    if row[7] in award_ids.keys():
        print('ERROR: non-unique award ID at row #' + str(i), ', award ID:', str(row[7]))
        award_ids[row[7]].append(i)
        remove_dupes = True
    else:
        award_ids[row[7]] = [int(i)]
    return award_ids, remove_dupes


# def collect_duplicate_rows(award_ids, modified_csv):
#     duplicate_awards = []
#     for award_id, csv_rows in award_ids.items():
#         if len(csv_rows) > 1:
#             for row in csv_rows:
#                 duplicate_row = modified_csv[row]
#                 duplicate_awards.append(duplicate_row)
#     return duplicate_awards


def write_csv(OUTFILE, modified_csv):
    with open(OUTFILE, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(modified_csv)


if __name__ == '__main__':
    with open(INFILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        #original_row_count = sum(1 for row in csv.reader(csv_file))
        modified_csv = []
        award_ids = {}
        original_row_count = 0
        for i, row in enumerate(reader):
            original_row_count += 1
            row = validate_abstract(row)
            award_ids, remove_dupes = validate_award_id(row, award_ids, i)
            if remove_dupes == True:
                continue # Row is not added to modified_csv
            validate_character_length(row, i)
            validate_type(row, i)
            modified_csv.append(row)
        print('Original length:', original_row_count)
        print('Deduplicated length:', len(modified_csv))
        #duplicate_awards = collect_duplicate_rows(award_ids, modified_csv)
        #answer = input('Please inspect the above errors. Continue? (Y/N)')
        #if answer == 'y' or 'Y' or 'yes' or 'Yes' or 'YES':
        write_csv(OUTFILE, modified_csv)
        print(OUTFILE)
        #if answer == 'n' or 'N' or 'no' or 'NO':
        #    write_csv(ERROR_FILE, duplicate_awards)