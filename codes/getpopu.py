import csv
import os

def getdatat(state):
    file_path=f'{os.getcwd()}/codes/population.csv'
    data_dict = []

    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            data_dict.append(dict(row))

    for datas in data_dict:
        if ((datas['State/UT']).lower()==state.lower()):
            return datas
