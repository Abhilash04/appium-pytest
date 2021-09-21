"""
This module is used for base page objects.
"""

from SupportLibraries.ui_helpers import UIHelpers


class BasePageObjects(UIHelpers):

    def navigate_back(self):
        self.driver.back()

    @classmethod
    def instance(cls, driver):
        and_cls = getattr(cls, '_ANDROID', cls)
        ios_cls = getattr(cls, '_IOS', cls)
        if driver._platform in ["android", "bs_android"]:
            return and_cls(driver)
        else:
            return ios_cls(driver)
