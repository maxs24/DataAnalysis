import plotly.express as px
import pandas as pd


INPUT_FILE_NAME = "data_out.csv"


def load_data():
    return pd.read_csv(INPUT_FILE_NAME)


# Разворачивание данных (название колонок в отдельный столбец)
def unstack_data(data, name):
    return data.set_index(first_column_name).unstack().reset_index(name=name).rename(columns={'level_0': 'Position'})


def proc_data(data):

    data_without_percent = unstack_data(data.drop(list(data.columns)[2::2], axis=1), 'Sum')
    data_only_percent = unstack_data(data.drop(list(data.columns)[1::2], axis=1), 'Percent')
    full_data = data_without_percent.join(data_only_percent['Percent'])
    return full_data


def view_data(data):
    fig = px.bar(data, x=first_column_name, y='Sum', hover_data=data.columns, color='Position')
    fig.show()


if __name__ == "__main__":
    loaded_data = load_data()
    first_column_name = loaded_data.columns[0]
    loaded_data = proc_data(loaded_data)

    view_data(loaded_data)
