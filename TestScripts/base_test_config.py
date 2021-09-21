import logging

import pytest

import FrameworkUtilities.logger_utility as log_utils
from FrameworkUtilities.execution_status_utility import ExecutionStatus
from PageObjects.po_home import HomePageObjects


@pytest.mark.usefixtures("driver")
class BaseTestConfig:
    log = log_utils.custom_logger(logging.INFO)

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.exe_status = ExecutionStatus(self.driver)
        self.home_page = HomePageObjects.instance(self.driver)
        yield "resource"
        self.driver.reset()
