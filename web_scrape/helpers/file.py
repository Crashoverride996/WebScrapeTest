import csv


def create_csv(name, header, rows):
    with open(name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for row in rows:
            row_list = zip(header, row)
            writer.writerow(dict(row_list))
