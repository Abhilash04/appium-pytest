""" This module is used for developing/ accessing data reader utility. """

import json
import os
import traceback

from ResourceFiles.constants import Identifiers


class DataReader:
    """
    This class includes basic reusable data helpers.
    """

    def __init__(self):
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.stage_test_data = os.path.join(self.cur_path, r"../TestData/stage_data.json")
        self.android_caps = os.path.join(self.cur_path, r"../DesiredCaps/android-local.json")
        self.ios_caps = os.path.join(self.cur_path, r"../DesiredCaps/ios-local.json")
        self.bs_android_caps = os.path.join(self.cur_path, r"../DesiredCaps/browserstack-android.json")
        self.bs_ios_caps = os.path.join(self.cur_path, r"../DesiredCaps/browserstack-ios.json")

    @staticmethod
    def load_json_data(json_file):
        """
        This methods is used for loading json file data
        :return: it returns json records
        """
        records = None

        # noinspection PyBroadException

        try:
            with open(json_file, "r") as read_file:
                records = json.load(read_file)
        except Exception as ex:
            traceback.print_exc(ex)

        return records

    def get_data(self, tc_id, data_key):
        """
        This method is used for returning column data specific to test case id/ name
        :param tc_id: it takes test case id/ name as input parameter
        :param data_key: it takes the name of the data_key for which value has to be returned
        :return:
        """
        value = None
        json_records = self.load_json_data(self.stage_test_data)

        try:
            if json_records is not None and json_records[tc_id] is not None:
                if data_key == Identifiers.RUNMODE.value:
                    value = json_records[tc_id][Identifiers.RUNMODE.value]
                else:
                    value = json_records[tc_id]['test_data'][data_key]
        except Exception as ex:
            traceback.print_exc(ex)

        return value

    def get_desired_caps(self, platform):
        desired_caps = {
            "android": self.load_json_data(self.android_caps),
            "ios": self.load_json_data(self.ios_caps),
            "bs_android": self.load_json_data(self.bs_android_caps),
            "bs_ios": self.load_json_data(self.bs_ios_caps)
        }
        return desired_caps.get(platform, self.load_json_data(self.android_caps))
