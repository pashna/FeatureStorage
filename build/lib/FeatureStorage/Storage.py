import os
from FeatureStorage.Feature import Feature


class Storage:

    def __init__(self, base_folder):
        """

        :param base_folder:
        """
        self._base_folder = base_folder
        self.features = {}

    def create_infrastructure(self):
        if not os.path.exists(self._base_folder):
            os.mkdir(self._base_folder)
        else:
            print("The folder {} already exist, won't be recreated".format(self._base_folder))

    def load(self):
        file_names = os.listdir(self._base_folder)
        feature_names = []
        for file_name in file_names:

            if not os.path.isfile(self._base_folder + os.sep + file_name):
                print(" is file name ", self._base_folder + os.sep + file_name)
                feature_names.append(file_name)

        for feature_name in feature_names:
            feature = Feature(self._base_folder, feature_name)
            feature.load()
            self.features[feature_name] = feature

    def join(self, df_train, df_test, exclude=[]):
        for feature_name, feature in self.features.items():
            if feature_name not in exclude:
                df_train, df_test = self.features[feature_name].join(df_train, df_test)

        return df_train, df_test
