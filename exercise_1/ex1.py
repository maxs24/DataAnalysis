import pandas as pd
from datetime import datetime

INPUT_FILE_NAME = "../data.csv"
OUTPUT_FILE_NAME = "table.csv"
INDEX_ACC = 1
INDEX_POS = 2
INDEX_AMOUNT = 3
INDEX_DT = 4


def load_data():
    return pd.read_csv(INPUT_FILE_NAME, sep=';')


def proc_data(data_csv):
    data_dict = dict()
    set_pos = set()
    data_all_amount = dict()
    summ = 0

    sorted_data_csv = data_csv.sort_values(by=["APPLICATION_DT"])

    # Создание словаря по датам и точкам из входных данных
    for row in sorted_data_csv.itertuples():
        date = datetime.strptime(row[INDEX_DT], "%Y-%m-%d %H:%M:%S")
        pos = int(row[INDEX_POS])
        amount = float(row[INDEX_AMOUNT])

        if date not in data_dict:
            data_dict[date] = dict()
            data_all_amount[date] = 0.0

        data_all_amount[date] += amount
        summ += amount

        set_pos.add(pos)
        if pos not in data_dict[date]:
            data_dict[date][pos] = [amount, "0%"]
        else:
            data_dict[date][pos][0] += amount

    # Задание процентов в словаре
    for key, value in data_dict.items():
        for position in set_pos:
            if position not in value:
                value[position] = [0, "0%"]
            else:
                value[position] = [value[position][0],
                                   str(round(value[position][0]/data_all_amount[key] * 100, 3)) + '%']

    return data_dict, set_pos


def value_to_name_column(value, percent=False):
    if percent:
        return str(value) + " (%)"
    else:
        return str(value)


# Создание датафрейма из словаря для дальнейшего экспорта в файл csv
def view_data(dict_data, list_positions):
    dict_for_dataframe = dict()
    dict_for_dataframe["Date"] = []
    for pos in list_positions:
        dict_for_dataframe[value_to_name_column(pos)] = []
        dict_for_dataframe[value_to_name_column(pos, True)] = []

    for key_date, value in dict_data.items():
        dict_for_dataframe["Date"].append(key_date)
        for key_pos, list_amount in value.items():
            dict_for_dataframe[value_to_name_column(key_pos)].append(list_amount[0])
            dict_for_dataframe[value_to_name_column(key_pos, True)].append(list_amount[1])

    return pd.DataFrame(dict_for_dataframe)


def export_to_file(export_dataframe):
    export_dataframe.to_csv(OUTPUT_FILE_NAME, index=False)


if __name__ == "__main__":
    data, pos_set = proc_data(load_data())
    pos_list = sorted(pos_set)

    data_table = view_data(data, pos_list)
    export_to_file(data_table)
