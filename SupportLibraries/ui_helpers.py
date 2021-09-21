"""
This module contains most of the reusable functions to support test cases.
"""

import logging
import os
from random import randint

import time
from appium.webdriver.common.mobileby import MobileBy
from builtins import staticmethod
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import FrameworkUtilities.logger_utility as log_utils


class UIHelpers:
    """
    UI Helpers class to contains all ui helper methods.
    """

    log = log_utils.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def get_locator_type(locator_type):
        """
        This method is used for getting locator type for element
        :param locator_type: it takes the locator type parameter ex- xpath, id
        :return: it returns the element identification based on locator type
        """
        locators = {
            "id": MobileBy.ID,
            "xpath": MobileBy.XPATH,
            "name": MobileBy.NAME,
            "class": MobileBy.CLASS_NAME,
            "link": MobileBy.LINK_TEXT,
            "partial_link": MobileBy.PARTIAL_LINK_TEXT,
            "accessibility_id": MobileBy.ACCESSIBILITY_ID
        }
        return locators.get(locator_type.lower(), MobileBy.ID)

    @staticmethod
    def wait_for_sync(seconds=5):
        time.sleep(seconds)

    @staticmethod
    def generate_random_phone_number():
        return '987' + str(randint(1234567, 9999999))

    @staticmethod
    def get_locator(locator_dict):
        return list(locator_dict.items())[0]

    def is_element_present(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method checks for presence of element & return the bollean value
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        """
        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.presence_of_element_located((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except WebDriverException:
            self.log.error(
                "Element is not present with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return False

    def verify_element_not_present(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to return the boolean value for element present
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element present or not
        """

        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.invisibility_of_element_located((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except WebDriverException:
            self.log.error(
                "Element is present with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return False

    def is_element_displayed(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to return the boolean value for element displayed
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element displayed or not
        """

        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.visibility_of_element_located((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except WebDriverException:
            self.log.error(
                "Element is not visible with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return False

    def is_element_clickable(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to return the boolean value for element clickable
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element clickable or not
        """

        try:
            WebDriverWait(self.driver, max_time_out, ignored_exceptions=[StaleElementReferenceException]).until(
                EC.element_to_be_clickable((self.get_locator_type(locator_type), locator_properties))
            )
            return True
        except WebDriverException:
            self.log.error(
                "Element is not clickable with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return False

    def is_element_checked(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to return the boolean value for element checked/ selected
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to the element present or not
        """
        flag = False

        if self.is_element_present(locator_properties, locator_type, max_time_out):
            element = self.get_element(locator_properties, locator_type, max_time_out)
            if element.is_selected():
                flag = True
            else:
                self.log.error(
                    "Element is not selected/ checked with locator_properties: " +
                    locator_properties + " and locator_type: " + locator_type)

        return flag

    def verify_elements_located(self, locator_dict, max_timeout=10):

        """
        This method is used to return the boolean value according to element presents on page
        :param locator_dict: this parameter takes the list of locator value and it's type
        :param max_timeout: this is the maximum time to wait for particular element
        :return: it returns the boolean value according to element presents on page
        """

        result = []
        for locator_prop in locator_dict.keys():
            prop_type = locator_dict[locator_prop]
            if self.is_element_present(locator_prop, prop_type, max_timeout):
                result.append(True)
            else:
                self.log.error(
                    "Element not found with locator_properties: " + locator_prop +
                    " and locator_type: " + locator_dict[locator_prop])
                result.append(False)

        if False in result:
            return False
        else:
            return True

    def get_element(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to get the element according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the element value
        """

        if self.is_element_present(locator_properties, locator_type, max_time_out):
            return self.driver.find_element(self.get_locator_type(locator_type), locator_properties)
        else:
            self.log.error(
                "Element not found with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return None

    def get_list_of_elements(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to get the element list according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the element values as a list
        """

        if self.is_element_present(locator_properties, locator_type, max_time_out):
            return self.driver.find_elements(locator_type, locator_properties)
        else:
            self.log.error(
                "Elements not found with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
            return None

    def get_text_from_element(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to get the element's inner text value according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the element inner text value
        """

        element = self.get_element(locator_properties, locator_type, max_time_out)
        result_text = element.text
        if len(result_text) == 0:
            result_text = element.get_attribute("innerText")
        elif len(result_text) != 0:
            self.log.info("The text is: '" + result_text + "'")
            result_text = result_text.strip()

        return result_text

    def get_attribute_value_from_element(self, attribute_name, locator_properties, locator_type="id", max_time_out=10):
        """
        This method is used to get the element's attribute value according to the locator type and property
        :param attribute_name: it takes the attribute name as parameter
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns the element attribute value
        """

        element = self.get_element(locator_properties, locator_type, max_time_out)
        attribute_value = element.get_attribute(attribute_name)
        if attribute_value is not None:
            self.log.info(attribute_name.upper() + " value is: " + attribute_value)
        else:
            self.log.error(attribute_name.upper() + " value is empty.")

        return attribute_value

    def mouse_click_action(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to perform mouse click action according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        if self.is_element_clickable(locator_properties, locator_type, max_time_out):
            element = self.get_element(locator_properties, locator_type, max_time_out)
            element.click()
            self.log.info("Clicked on the element with locator_properties: "
                          + locator_properties + " and locator_type: " + locator_type)
        else:
            self.log.error("Unable to click on the element with locator_properties: "
                           + locator_properties + " and locator_type: " + locator_type)

    def mouse_click_action_on_element_present(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to perform mouse click action according to the locator type and property
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        if self.is_element_present(locator_properties, locator_type, max_time_out):
            element = self.get_element(locator_properties, self.get_locator_type(locator_type), max_time_out)
            element.click()
            self.log.info(
                "Clicked on the element with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
        else:
            self.log.error("Unable to click on the element with locator_properties: "
                           + locator_properties + " and locator_type: " + locator_type)

    def move_to_element_and_click(self, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used when element is not receiving the direct click
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        """

        if self.is_element_clickable(locator_properties, locator_type, max_time_out):
            element = self.get_element(locator_properties, locator_type, max_time_out)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            self.log.info(
                "Clicked on the element with locator_properties: " + locator_properties + " and locator_type: "
                + locator_type)
        else:
            self.log.error("Unable to click on the element with locator_properties: "
                           + locator_properties + " and locator_type: " + locator_type)

    def enter_text_action(self, text_value, locator_properties, locator_type="id", max_time_out=10):

        """
        This method is used to enter the value in text input field
        :param text_value: it takes input string as parameter
        :param locator_properties: it takes locator string as parameter
        :param locator_type: it takes locator type as parameter
        :param max_time_out: this is the maximum time to wait for particular element
        :return: it returns nothing
        :return:
        """

        element = self.get_element(locator_properties, locator_type, max_time_out)
        element.clear()
        element.send_keys(text_value)
        self.log.info(
            "Sent data to the element with locator_properties: " + locator_properties + " and locator_type: "
            + locator_type)
        return element

    def verify_text_contains(self, actual_text, expected_text):

        """
        This method verifies that actual text in the expected string 
        :param actual_text: it takes actual keyword/ substring
        :param expected_text: it takes the string value to search actual keyword in it
        :return: it return boolean value according to verification
        """

        if expected_text.lower() in actual_text.lower():
            self.log.info("### VERIFICATION TEXT CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION TEXT DOES NOT CONTAINS !!!")
            self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
            self.log.info("Expected Text From Application Web UI --> :: " + expected_text)
            return False

    def verify_text_match(self, actual_text, expected_text):

        """
        This method verifies the exact match of actual text and expected text
        :param actual_text: it takes actual string value
        :param expected_text: it takes the expected string value to match with
        :return: it return boolean value according to verification
        """

        if expected_text.lower() == actual_text.lower():
            self.log.info("### VERIFICATION TEXT MATCHED !!!")
            return True
        else:
            self.log.error("### VERIFICATION TEXT DOES NOT MATCHED !!!")
            self.log.info("Actual Text From Application Web UI --> :: " + actual_text)
            self.log.info("Expected Text From Application Web UI --> :: " + expected_text)
            return False

    def take_screenshots(self, file_name_initials):

        """
        This method takes screen shot for reporting
        :param file_name_initials: it takes the initials for file name
        :return: it returns the destination directory of screenshot
        """

        file_name = file_name_initials + "." + str(round(time.time() * 1000)) + ".png"
        cur_path = os.path.abspath(os.path.dirname(__file__))
        screenshot_directory = os.path.join(cur_path, r"../Logs/Screenshots/")

        destination_directory = os.path.join(screenshot_directory, file_name)

        try:
            if not os.path.exists(screenshot_directory):
                os.makedirs(screenshot_directory)
            self.driver.save_screenshot(destination_directory)
            self.log.info("Screenshot saved to directory: " + destination_directory)
        except Exception as ex:
            self.log.error("### Exception occurred:: ", ex)

        return destination_directory

    def vertical_scroll(self, scroll_view, class_name, text):
        """
        This function is used for vertical scroll
        :param scroll_view: class name for scrollView
        :param class_name: class name for text view
        :param text: text of the element
        :return: this function returns nothing
        """
        try:
            self.driver.find_element_by_android_uiautomator(
                "new UiScrollable(new UiSelector().scrollable(true)" +
                ".className(\"" + scroll_view + "\")).scrollIntoView(new UiSelector()" +
                ".className(\"" + class_name + "\").text(\"" + text + "\"))")
            self.log.info("Vertically scrolling into the view.")

        except Exception as ex:
            self.log.error("Exception occurred while vertically scrolling into the view: ", ex)

    def horizontal_scroll(self, scroll_view, class_name, text):
        """
        This function is used for horizontal scroll
        :param scroll_view: class name for scroll view
        :param class_name: class name for text view
        :param text: text of the element
        :return: this function returns nothing
        """
        try:
            self.driver.find_element_by_android_uiautomator(
                "new UiScrollable(new UiSelector().scrollable(true)" +
                ".className(\"" + scroll_view + "\")).setAsHorizontalList().scrollIntoView(new UiSelector()" +
                ".className(\"" + class_name + "\").text(\"" + text + "\"))")
            self.log.info("Horizontally scrolling into the view.")

        except Exception as ex:
            self.log.error("Exception occurred while horizontally scrolling into the view: ", ex)
