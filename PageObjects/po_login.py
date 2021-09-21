"""
This module is used for login page objects.
"""

from ResourceFiles.constants import Identifiers
from PageObjects.po_base import BasePageObjects


class LoginPageObjects(BasePageObjects):
    """
    This class defines the element identifiers and methods for login page.
    """

    # Locators
    login_title = {"//*[@name='Login']": Identifiers.XPATH.value}
    username_field = {"//*[@name='username' and @value='Username']": Identifiers.XPATH.value}
    password_field = {"//*[@name='password' and @value='Password']": Identifiers.XPATH.value}

    def verify_login_screen_elements(self):
        """
        This function is used to verify all the elements present on the login screen
        :return: this function returns boolean status of element located
        """

        locator_dict = {}
        locator_dict.update(self.login_title)
        locator_dict.update(self.username_field)
        locator_dict.update(self.password_field)

        result = self.verify_elements_located(locator_dict)

        if not result:
            self.log.error("Login screen element verification failed.")

        return result

    def navigate_to_home_screen(self):
        """
        This function is used to navigate to home screen
        :return: instance of registration page objects
        """
        self.navigate_back()


class AndLoginPageObjects(LoginPageObjects):
    # Locators
    login_title = {"(//*[@text='Login'])[1]": Identifiers.XPATH.value}
    username_field = {"//*[@text='Username']": Identifiers.XPATH.value}
    password_field = {"//*[@text='Password']": Identifiers.XPATH.value}


class IOSLoginPageObjects(LoginPageObjects):
    # Locators
    login_title = {"Login": Identifiers.ACCESSIBILITY_ID.value}


LoginPageObjects._ANDROID = AndLoginPageObjects
LoginPageObjects._IOS = IOSLoginPageObjects
