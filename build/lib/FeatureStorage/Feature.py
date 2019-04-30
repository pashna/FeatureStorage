import os
import pandas as pd
import json
from datetime import datetime


class Feature:

    def __init__(self, base_path, feature_name, key='index'):
        self._base_path = base_path
        self._feature_name = feature_name
        self._feature_folder = self._base_path + os.sep + self._feature_name
        self._key = key
        self.storage = {}

    def set_files(self, file_dict):
        for name, obj in file_dict.items():
            self.storage[name] = obj

    def load(self):
        files = os.listdir(self._feature_folder)

        for full_file_name in files:
            self.storage[full_file_name] = self._load_file(full_file_name)

    def save(self):
        if not os.path.exists(self._feature_folder):
            os.mkdir(self._feature_folder)

        meta = {"updated_time": str(datetime.today()),
                "key": self._key}
        try:
            for name, obj in self.storage.items():
                self._save_file(obj, name)

            self._save_file(meta, 'meta.json')
        except Exception as e:
            print(str(e))
            meta['updated_time'] = "Something went wrong: {}".format(str(e))
            self._save_file(meta, 'meta.json')
        self.storage['meta.json'] = meta

    def join(self, df_train, df_test):
        print(list(self.storage.keys()))
        key = self.storage['meta.json']['key']

        if key == 'index':
            df_train = df_train.join(self.storage['train.csv'])
            df_test = df_test.join(self.storage['test.csv'])
        else:
            df_train = df_train.merge(self.storage['train.csv'], on=key, how='left')
            df_test = df_test.merge(self.storage['test.csv'], on=key, how='left')

        return df_train, df_test

    def _load_file(self, name):
        file_name, file_type = self.__get_name_and_type(name)

        if file_type == 'csv':
            obj = pd.read_csv(self._feature_folder + os.sep + name)
        elif file_type == 'json':
            with open(self._feature_folder + os.sep + name, 'r') as file:
                obj = json.load(file)
        else:
            with open(self._feature_folder + os.sep + name, 'r') as file:
                obj = file.read()

        return obj

    def _save_file(self, obj, name):
        file_name, file_type = self.__get_name_and_type(name)

        if file_type == 'csv':
            obj.to_csv(self._feature_folder + os.sep + name, index=0)
        elif file_type == 'json':
            with open(self._feature_folder + os.sep + name, 'w') as file:
                json.dump(obj, file)
        else:
            with open(self._feature_folder + os.sep + name, 'w') as file:
                file.write(obj)

    def __get_name_and_type(self, path):
        if os.sep in path:
            file_name = path.split(os.sep)[-1]
        else:
            file_name = path

        file_type = file_name.split('.')[-1]
        return file_name, file_type
