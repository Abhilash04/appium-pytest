"""
This module is used for welcome page objects.
"""

from ResourceFiles.constants import Identifiers
from PageObjects.po_base import BasePageObjects
from PageObjects.po_login import LoginPageObjects
from PageObjects.po_echo import EchoBoxPageObjects


class HomePageObjects(BasePageObjects):
    """
    This class defines the element identifiers and methods for home page.
    """

    # Locators
    echo_box_link = {"//*[@text='Echo Box']": Identifiers.XPATH.value}
    login_link = {"//*[@text='Login Screen']": Identifiers.XPATH.value}
    echo_box_save_button = {"(//*[@name='messageSaveBtn'])[2]": Identifiers.XPATH.value}
    login_button = {"(//*[@name='loginBtn'])[2]": Identifiers.XPATH.value}

    def verify_home_screen_elements(self):
        """
        This function is used to verify all the elements present on the welcome screen
        :return: this function returns boolean status of element located
        """

        locator_dict = {}
        locator_dict.update(self.echo_box_link)
        locator_dict.update(self.login_link)
        result = self.verify_elements_located(locator_dict)

        if not result:
            self.log.error("Home screen element verification failed.")

        return result

    def navigate_to_echo_box(self):
        """
        This function is used to navigate to echo box screen
        :return: instance of echo box screen
        """

        echo_box_link_prop = self.get_locator(self.echo_box_link)
        echo_box_save_button_prop = self.get_locator(self.echo_box_save_button)
        self.mouse_click_action(echo_box_link_prop[0],
                                echo_box_link_prop[1])
        self.is_element_displayed(echo_box_save_button_prop[0],
                                  echo_box_save_button_prop[1])
        return EchoBoxPageObjects.instance(self.driver)

    def navigate_to_login_screen(self):
        """
        This function is used to navigate to login screen
        :return: instance of login screen
        """
        login_link_prop = self.get_locator(self.login_link)
        login_button_prop = self.get_locator(self.login_button)
        self.mouse_click_action(login_link_prop[0],
                                login_link_prop[1])
        self.is_element_displayed(login_button_prop[0],
                                  login_button_prop[1])
        return LoginPageObjects.instance(self.driver)


class AndHomePageObjects(HomePageObjects):
    login_button = {"(//*[@text='Login'])[2]": Identifiers.XPATH.value}


class IOSHomePageObjects(HomePageObjects):
    # Locators
    echo_box_link = {"Echo Box": Identifiers.ACCESSIBILITY_ID.value}
    login_link = {"Login Screen": Identifiers.ACCESSIBILITY_ID.value}


HomePageObjects._ANDROID = AndHomePageObjects
HomePageObjects._IOS = IOSHomePageObjects
