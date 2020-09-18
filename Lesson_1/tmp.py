from pathlib import Path
import json


class Getter:

    def __init__(self):
        self.file_path = file_path


    def get_categories(self):

        with open(file_path, 'r') as file:
            json_data = file.read()
            tmp = json.loads(json_data)
            parent_group_code = tmp.get('parent_group_code')
            print(parent_group_code)


file_path = Path('data').joinpath(f"Канцелярские товары.json")
# file_path = 'C:/Users/Nikolas/PycharmProjects/GB_parse/Lesson_1/data/Канцелярские товары.json'
print(file_path)

a = Getter
a.get_categories(file_path)