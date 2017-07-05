# -*- coding: utf-8 -*-
from datetime import datetime

from pynanaco.locators import *


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    _locator = LoginPageLocators

    def input_nanaco_number(self, nanaco_number):
        element = self.driver.find_element(*self._locator.INPUT_NANACO_NUMBER)
        element.send_keys(nanaco_number)

    def input_card_number(self, card_number):
        element = self.driver.find_element(*self._locator.INPUT_CARD_NUMBER)
        element.send_keys(card_number)

    def input_login_password(self, password):
        element = self.driver.find_element(*self._locator.INPUT_LOGIN_PWD)
        element.send_keys(password)

    def click_login_by_card(self):
        element = self.driver.find_element(*self._locator.BUTTON_LOGIN_BY_CARD)
        element.click()
        return MenuPage(self.driver)

    def click_login_by_password(self):
        element = self.driver.find_element(*self._locator.BUTTON_LOGIN_BY_PWD)
        element.click()
        return MenuPage(self.driver)


class AfterLogoutPage(BasePage):
    _locator = AfterLogoutPageLocators

    def click_back_to_login(self):
        element = self.driver.find_element(*self._locator.BUTTON_BACK_TO_LOGIN)
        element.click()
        return LoginPage(self.driver)


class BaseMenuPage(BasePage):
    _locator = BaseMenuPageLocators

    def click_logout(self):
        element = self.driver.find_element(*self._locator.BUTTON_LOGOUT)
        element.click()
        return AfterLogoutPage(self.driver)


class MenuPage(BaseMenuPage):
    _locator = MenuPageLocators

    def click_credit_charge(self):
        element = self.driver.find_element(*self._locator.BUTTON_CREDIT_CHARGE)
        element.click()
        return CreditChargePasswordAuthPage(self.driver)

    def click_top_menu_credit_charge(self):
        element = self.driver.find_element(*self._locator.TOP_MENU_CREDIT_CHARGE)
        element.click()
        return CreditChargePasswordAuthPage(self.driver)


class CreditChargeGuidePage(BaseMenuPage):
    _locator = CreditChargeGuidePageLocators

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegPage(self.driver)


class CreditChargePasswordAuthPage(BaseMenuPage):
    _locator = CreditChargePasswordAuthPageLocators

    def input_credit_charge_password(self, password):
        element = self.driver.find_element(*self._locator.INPUT_CREDIT_CHARGE_PWD)
        element.send_keys(password)

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeMainPage(self.driver)


class CreditChargeRegPage(BaseMenuPage):
    _locator = CreditChargeRegPageLocators

    def click_agree(self):
        element = self.driver.find_element(*self._locator.BUTTON_AGREE)
        element.click()
        return CreditChargeRegInput1Page(self.driver)


class CreditChargeRegInput1Page(BaseMenuPage):
    _locator = CreditChargeRegInput1PageLocators

    def input_credit_card(self, number: str, expire_month: str, expire_year: str, code: str, phone: str):
        number = str(number)
        element = self.driver.find_element(*self._locator.INPUT_NUMBER_1)
        element.send_keys(number[0:4])
        element = self.driver.find_element(*self._locator.INPUT_NUMBER_2)
        element.send_keys(number[4:8])
        element = self.driver.find_element(*self._locator.INPUT_NUMBER_3)
        element.send_keys(number[8:12])
        element = self.driver.find_element(*self._locator.INPUT_NUMBER_4)
        element.send_keys(number[12:16])

        element = self.driver.find_element(*self._locator.INPUT_EXPIRE_MONTH)
        element.send_keys(expire_month)
        element = self.driver.find_element(*self._locator.INPUT_EXPIRE_YEAR)
        element.send_keys(expire_year[2:4])

        element = self.driver.find_element(*self._locator.INPUT_CODE)
        element.send_keys(code)

        element = self.driver.find_element(*self._locator.INPUT_PHONE)
        element.send_keys(phone)

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegInput2Page(self.driver)


class CreditChargeRegInput2Page(BaseMenuPage):
    _locator = CreditChargeRegInput2PageLocators

    def input_profile(self, name: str, birthday: datetime, password: str, mail: str, send_information: str = '2'):
        element = self.driver.find_element(*self._locator.INPUT_NAME)
        element.send_keys(name)

        element = self.driver.find_element(*self._locator.INPUT_BIRTH_YEAR)
        element.send_keys(birthday.year)
        element = self.driver.find_element(*self._locator.INPUT_BIRTH_MONTH)
        element.send_keys(birthday.month)
        element = self.driver.find_element(*self._locator.INPUT_BIRTH_DAY)
        element.send_keys(birthday.day)

        element = self.driver.find_element(*self._locator.INPUT_PWD)
        element.send_keys(password)
        element = self.driver.find_element(*self._locator.INPUT_PWD_CONF)
        element.send_keys(password)

        element = self.driver.find_element(*self._locator.INPUT_EMAIL)
        element.send_keys(mail)
        element = self.driver.find_element(*self._locator.INPUT_EMAIL_CONF)
        element.send_keys(mail)

        element = self.driver.find_element(*self._locator.INPUT_INFO_SEND_FLAG)
        element.send_keys(send_information)

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegConfirmPage(self.driver)


class CreditChargeRegConfirmPage(BaseMenuPage):
    _locator = CreditChargeRegConfirmPageLocators

    def click_confirm(self):
        element = self.driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return SecurePage(self.driver)


class SecurePage(BasePage):
    _locator = SecurePageLocators

    def input_secure_code(self, secure_code: str):
        element = self.driver.find_element(*self._locator.INPUT_SECURE_CODE)
        element.send_keys(secure_code)

    def click_send(self):
        element = self.driver.find_element(*self._locator.BUTTON_SEND)
        element.click()
        return CreditChargeRegSucceedPage(self.driver)


class CreditChargeRegSucceedPage(BaseMenuPage):
    _locator = CreditChargeRegSucceedPageLocators

    def click_back_to_home(self):
        element = self.driver.find_element(*self._locator.BUTTON_BACK_TO_HOME)
        element.click()
        return MenuPage(self.driver)


class CreditChargeMainPage(BaseMenuPage):
    _locator = CreditChargeMainPageLocators

    def click_charge(self):
        element = self.driver.find_element(*self._locator.BUTTON_CHARGE)
        element.click()
        return CreditChargeInputPage(self.driver)

    def click_cancel(self):
        element = self.driver.find_element(*self._locator.BUTTON_CANCEL)
        element.click()
        return CreditChargeCancelInputPage(self.driver)


class CreditChargeInputPage(BaseMenuPage):
    _locator = CreditChargeInputPageLocators

    def input_amount(self, value):
        element = self.driver.find_element(*self._locator.INPUT_AMOUNT)
        element.send_keys(value)

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeConfirmPage(self.driver)


class CreditChargeConfirmPage(BaseMenuPage):
    _locator = CreditChargeConfirmPageLocators

    def click_back(self):
        element = self.driver.find_element(*self._locator.BUTTON_BACK)
        element.click()
        return CreditChargeInputPage(self.driver)

    def click_confirm(self):
        element = self.driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return CreditChargeSucceedPage(self.driver)


class CreditChargeSucceedPage(BaseMenuPage):
    _locator = CreditChargeSucceedPageLocators

    def click_back_to_top(self):
        element = self.driver.find_element(*self._locator.BUTTON_BACK_TO_TOP)
        element.click()
        return CreditChargeMainPage(self.driver)


class CreditChargeCancelInputPage(BaseMenuPage):
    _locator = CreditChargeCancelInputPageLocators

    def input_credit_charge_password(self, password):
        element = self.driver.find_element(*self._locator.INPUT_CREDIT_CHARGE_PWD)
        element.send_keys(password)

    def click_next(self):
        element = self.driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeCancelConfirmPage(self.driver)


class CreditChargeCancelConfirmPage(BaseMenuPage):
    _locator = CreditChargeCancelConfirmPageLocators

    def click_confirm(self):
        element = self.driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return CreditChargeCancelSucceedPage(self.driver)


class CreditChargeCancelSucceedPage(BaseMenuPage):
    _locator = CreditChargeCancelSucceedPageLocators

    def click_back_to_home(self):
        element = self.driver.find_element(*self._locator.BUTTON_BACK_TO_HOME)
        element.click()
        return MenuPage(self.driver)


class CreditChargeErrorPage(BasePage):
    _locator = CreditChargeErrorPageLocators

    def get_alert_msg(self):
        element = self.driver.find_element(*self._locator.ALERT)
        return element.text
