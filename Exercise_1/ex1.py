import pandas as pd
from datetime import datetime

FILE_NAME = "../data.csv"
INDEX_ACC = 0
INDEX_POS = 1
INDEX_AMOUNT = 2
INDEX_DT = 3


def load_data():
    return pd.read_csv(FILE_NAME)


def proc_data(data_csv):
    data_dict = dict()
    for row in data_csv.itertuples():
        row_mas = row[1].split(";")
        date = datetime.strptime(row_mas[INDEX_DT], "%Y-%m-%d %H:%M:%S")
        if date not in data_dict:
            data_dict[date] = dict()

        pos = row_mas[INDEX_POS]
        if pos not in data_dict:
            data_dict[date][pos] = float(row_mas[INDEX_AMOUNT])
        else:
            data_dict[date][pos] += float(row_mas[INDEX_AMOUNT])

    return data_dict


if __name__ == '__main__':

    print(proc_data(load_data()))

