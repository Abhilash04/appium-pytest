""" This module contains the singleton driver instance implementation"""

import logging
import os

from appium import webdriver

from FrameworkUtilities.data_reader_utility import DataReader
from FrameworkUtilities.logger_utility import custom_logger


class DriverFactory:
    """
    This class contains the reusable methods for getting the driver instances
    """
    log = custom_logger(logging.INFO)
    data_reader = DataReader()

    def __init__(self, platform):
        self.platform = platform
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.local_appium_server = "http://127.0.0.1:4723/wd/hub"
        self.browser_stack_server = "http://hub-cloud.browserstack.com/wd/hub"

    def get_driver_instance(self):
        desired_caps = self.data_reader.get_desired_caps(self.platform)
        server = {
            "android": self.local_appium_server,
            "ios": self.local_appium_server,
            "bs_android": self.browser_stack_server,
            "bs_ios": self.browser_stack_server
        }

        if self.platform not in ["android", "ios"]:
            desired_caps['browserstack.user'] = os.getenv('BS_USERNAME')
            desired_caps['browserstack.key'] = os.getenv('BS_KEY')
            return webdriver.Remote(
                command_executor=server.get(self.platform, self.local_appium_server),
                desired_capabilities=desired_caps)
        else:
            app_location = os.path.join(self.cur_path, r"../MobileApp/", desired_caps['app'])
            desired_caps['app'] = app_location
            return webdriver.Remote(
                command_executor=server.get(self.platform, self.local_appium_server),
                desired_capabilities=desired_caps)
