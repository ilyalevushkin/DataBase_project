import json
import os.path

from json_converter import JsonConverter


def get_file_name_to_read(model_str):
    return str(input("Введите имя файла, откуда будет загружаться информация (формат csv) для модели " + model_str + ": "))


def get_file_name_to_write(model_str):
    return str(input("Введите имя файла, куда будет загружаться json-информация для модели " + model_str + ": "))


def put_file_name_to_correct_path(path, file_name):
    return path + file_name

def load_info_to_json(model_str):
    file_name = get_file_name_to_read(model_str)

    file_name = put_file_name_to_correct_path("./data/", file_name)

    f = open(file_name, 'r')

    file_lines = f.readlines()
    f.close()

    file_name = get_file_name_to_write(model_str)

    file_name = put_file_name_to_correct_path("../virus_app/fixtures/", file_name)

    json_converter = JsonConverter()

    json_data_mas = json_converter.get_json_data_mas(file_lines, model_str)

    file_exist = os.path.exists(file_name)

    with open(file_name, "a") as write_file:
        if (not file_exist):
            write_file.write("[")
        for json_data in json_data_mas:
            json.dump(json_data, write_file)
            write_file.write(",")