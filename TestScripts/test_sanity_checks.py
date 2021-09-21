""" This module contains the home screen test cases."""

import allure
import sys
from ResourceFiles.group_marks import sanity
from TestScripts.base_test_config import BaseTestConfig


@allure.story('[TestApp] - Welcome Sanity Tests')
@allure.feature('Android App Welcome Tests')
class TestSanityChecks(BaseTestConfig):
    """ This class contains the home page sanity test cases."""
    @sanity
    @allure.testcase("Verify Home Screen Scenarios")
    def test_sanity_101(self, setup_teardown):
        """
        This test is validating the home screen elements & successful
        navigation from welcome screen to login screen
        :return: return test status
        """
        test_name = sys._getframe().f_code.co_name

        self.log.info("###### TEST EXECUTION STARTED :: " + test_name + " ######")

        with allure.step("verify presence of home screen elements"):
            self.exe_status.mark_final(test_step="verify presence of home screen elements",
                                       result=self.home_page.verify_home_screen_elements())

        with allure.step("verify presence of login screen elements"):
            login_page = self.home_page.navigate_to_login_screen()
            self.exe_status.mark_final(test_step="verify presence of home screen elements",
                                       result=login_page.verify_login_screen_elements())
