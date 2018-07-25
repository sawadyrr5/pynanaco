# -*- coding: utf-8 -*-
from pynanaco.locators import *

import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)


class _BasePage:
    _title = None

    def __init__(self, driver):
        self._driver = driver


class PageUnmatchError(Exception):
    pass


class BasePage(_BasePage):
    _title = None

    def is_current(self):
        return True


class LoginPage(BasePage):
    """

    """
    _locator = LoginPageLocators
    _title = 'nanaco / ログイン'

    def input_nanaco_number(self, nanaco_number):
        element = self._driver.find_element(*self._locator.INPUT_NANACO_NUMBER)
        element.send_keys(nanaco_number)

    def input_card_number(self, card_number):
        element = self._driver.find_element(*self._locator.INPUT_CARD_NUMBER)
        element.send_keys(card_number)

    def input_login_password(self, password):
        element = self._driver.find_element(*self._locator.INPUT_LOGIN_PWD)
        element.send_keys(password)

    def click_login_by_card(self):
        element = self._driver.find_element(*self._locator.BUTTON_LOGIN_BY_CARD)
        element.click()
        return MenuPage(self._driver)

    def click_login_by_password(self):
        element = self._driver.find_element(*self._locator.BUTTON_LOGIN_BY_PWD)
        element.click()
        return MenuPage(self._driver)

    # TODO:
    def is_login_succeed(self):
        element = self._driver.find_element(*self._locator.TEXT_LOGIN_ERROR)
        print(
            element
        )


class AfterLogoutPage(BasePage):
    _locator = AfterLogoutPageLocators
    _title = 'nanaco / ログアウト'

    def click_back_to_login(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK_TO_LOGIN)
        element.click()
        return LoginPage(self._driver)


class BaseMenuPage(BasePage):
    _locator = BaseMenuPageLocators
    _title = 'nanaco / 会員メニュー'

    def click_logout(self):
        element = self._driver.find_element(*self._locator.BUTTON_LOGOUT)
        element.click()
        return AfterLogoutPage(self._driver)

    def click_logo(self):
        element = self._driver.find_element(*self._locator.LOGO)
        element.click()
        return MenuPage(self._driver)


class MenuPage(BaseMenuPage):
    _locator = MenuPageLocators
    _title = 'nanaco / 会員メニュー'

    def click_credit_charge(self):
        element = self._driver.find_element(*self._locator.BUTTON_CREDIT_CHARGE)
        element.click()
        return CreditChargePasswordAuthPage(self._driver)

    def click_top_menu_credit_charge(self):
        element = self._driver.find_element(*self._locator.TOP_MENU_CREDIT_CHARGE)
        element.click()
        return CreditChargePasswordAuthPage(self._driver)

    def click_register_gift(self):
        element = self._driver.find_element(*self._locator.BUTTON_REGISTER_GIFT)
        element.click()
        return RegisterGiftPage(self._driver)

    def text_balance_card(self):
        element = self._driver.find_element(*self._locator.TEXT_BALANCE_CARD)
        return int(element.text.replace('円', '').replace(',', ''))

    def text_balance_center(self):
        element = self._driver.find_element(*self._locator.TEXT_BALANCE_CENTER)
        return int(element.text.replace('円', '').replace(',', ''))


class CreditChargeGuidePage(BaseMenuPage):
    _locator = CreditChargeGuidePageLocators
    _title = 'nanaco / クレジットチャージ・オートチャージのご案内'

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegPage(self._driver)


class CreditChargePasswordAuthPage(BaseMenuPage):
    _locator = CreditChargePasswordAuthPageLocators
    _title = 'nanaco / クレジットチャージ　パスワード認証画面'

    def input_credit_charge_password(self, password):
        element = self._driver.find_element(*self._locator.INPUT_CREDIT_CHARGE_PWD)
        element.send_keys(password)

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeMainPage(self._driver)


class CreditChargeRegPage(BaseMenuPage):
    _locator = CreditChargeRegPageLocators
    _title = 'nanaco / クレジットカードの事前登録（特約確認）'

    def click_agree(self):
        element = self._driver.find_element(*self._locator.BUTTON_AGREE)
        element.click()
        return CreditChargeRegInput1Page(self._driver)


class CreditChargeRegInput1Page(BaseMenuPage):
    _locator = CreditChargeRegInput1PageLocators
    _title = 'nanaco / クレジットカードの事前登録 入力（1/2）'

    def input_credit_card(self, number: str, expire_month: str, expire_year: str, code: str):
        element = self._driver.find_element(*self._locator.INPUT_NUMBER_1)
        element.send_keys(number[0:4])
        element = self._driver.find_element(*self._locator.INPUT_NUMBER_2)
        element.send_keys(number[4:8])
        element = self._driver.find_element(*self._locator.INPUT_NUMBER_3)
        element.send_keys(number[8:12])
        element = self._driver.find_element(*self._locator.INPUT_NUMBER_4)
        element.send_keys(number[12:16])

        element = self._driver.find_element(*self._locator.INPUT_EXPIRE_MONTH)
        element.send_keys(expire_month)

        element = self._driver.find_element(*self._locator.INPUT_EXPIRE_YEAR)
        element.send_keys(expire_year)

        element = self._driver.find_element(*self._locator.INPUT_CODE)
        element.send_keys(code)

    def input_phone(self, phone):
        element = self._driver.find_element(*self._locator.INPUT_PHONE)
        element.send_keys(phone)

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegInput2Page(self._driver)


class CreditChargeRegInput2Page(BaseMenuPage):
    _locator = CreditChargeRegInput2PageLocators
    _title = 'nanaco / クレジットカードの事前登録 入力（2/2）'

    def input_profile(self, name: str, birth_year: str, birth_month: str, birth_day: str, password: str, mail: str,
                      send_info: str = '2'):
        element = self._driver.find_element(*self._locator.INPUT_NAME)
        element.send_keys(name)

        element = self._driver.find_element(*self._locator.INPUT_BIRTH_YEAR)
        element.send_keys(birth_year)
        element = self._driver.find_element(*self._locator.INPUT_BIRTH_MONTH)
        element.send_keys(birth_month)
        element = self._driver.find_element(*self._locator.INPUT_BIRTH_DAY)
        element.send_keys(birth_day)

        element = self._driver.find_element(*self._locator.INPUT_PWD)
        element.send_keys(password)
        element = self._driver.find_element(*self._locator.INPUT_PWD_CONF)
        element.send_keys(password)

        element = self._driver.find_element(*self._locator.INPUT_EMAIL)
        element.send_keys(mail)
        element = self._driver.find_element(*self._locator.INPUT_EMAIL_CONF)
        element.send_keys(mail)

        element = self._driver.find_element(*self._locator.INPUT_INFO_SEND_FLAG)
        element.send_keys(send_info)

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeRegConfirmPage(self._driver)


class CreditChargeRegConfirmPage(BaseMenuPage):
    _locator = CreditChargeRegConfirmPageLocators
    _title = 'nanaco / クレジットカードの事前登録　確認'

    def click_confirm(self):
        element = self._driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return SecurePage(self._driver)


class SecurePage(BasePage):
    _locator = SecurePageLocators

    def input_secure_code(self, secure_code):
        if 'VISA' in self._driver.title:
            element = self._driver.find_element(*self._locator.INPUT_SECURE_CODE_VISA)

        elif 'J/Secure' in self._driver.title:
            element = self._driver.find_element(*self._locator.INPUT_SECURE_CODE_JCB)

        else:
            element = None

        element.send_keys(secure_code)

    def click_send(self):
        if 'VISA' in self._driver.title:
            element = self._driver.find_element(*self._locator.BUTTON_SEND_VISA)

        elif 'J/Secure' in self._driver.title:
            element = self._driver.find_element(*self._locator.BUTTON_SEND_JCB)

        else:
            element = None

        element.click()
        return CreditChargeRegSucceedPage(self._driver)


class CreditChargeRegSucceedPage(BaseMenuPage):
    _locator = CreditChargeRegSucceedPageLocators
    _title = 'nanaco / クレジットカードの事前登録　完了'

    def click_back_to_home(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK_TO_HOME)
        element.click()
        return MenuPage(self._driver)


class CreditChargeMainPage(BaseMenuPage):
    _locator = CreditChargeMainPageLocators
    _title = 'nanaco / nanacoクレジットチャージ'

    def click_charge(self):
        element = self._driver.find_element(*self._locator.BUTTON_CHARGE)
        element.click()
        return CreditChargeInputPage(self._driver)

    def click_cancel(self):
        element = self._driver.find_element(*self._locator.BUTTON_CANCEL)
        element.click()
        return CreditChargeCancelInputPage(self._driver)

    def click_history(self):
        element = self._driver.find_element(*self._locator.BUTTON_HISTORY)
        element.click()
        return CreditChargeHistoryPage(self._driver)

    def click_change_password(self):
        element = self._driver.find_element(*self._locator.BUTTON_CHANGE_CREDIT_CARD)
        element.click()
        return CreditChargePasswordChangeInputPage(self._driver)

    def click_change_credit_card(self):
        element = self._driver.find_element(*self._locator.BUTTON_CHANGE_CREDIT_CARD)
        element.click()
        return CreditChargeRegInput1Page(self._driver)

    def text_credit_card(self):
        element = self._driver.find_element(*self._locator.TEXT_CREDIT_CARD)
        return element.text.replace('登録クレジットカード：', '')


class CreditChargePasswordChangeInputPage(BaseMenuPage):
    _locator = CreditChargePasswordChangeInputPageLocators

    def input_old_password(self, password):
        element = self._driver.find_element(*self._locator.INPUT_OLD_PASSWORD)
        element.send_keys(password)

    def input_new_password(self, password):
        element = self._driver.find_element(*self._locator.INPUT_NEW_PASSWORD)
        element.send_keys(password)

        element = self._driver.find_element(*self._locator.INPUT_NEW_PASSWORD_CONF)
        element.send_keys(password)

    def click(self):
        element = self._driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return CreditChargePasswordChangeSucceedPage(self._driver)


class CreditChargePasswordChangeSucceedPage(BaseMenuPage):
    _locator = CreditChargePasswordChangeSucceedPageLocators

    def click_confirm(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK_TO_CREDIT_CHARGE_TOP)
        element.click()
        return CreditChargeMainPage(self._driver)


class CreditChargeHistoryPage(BaseMenuPage):
    _locator = CreditChargeHistoryPageLocators

    def text_charged_count(self):
        element = self._driver.find_element(*self._locator.TEXT_CHARGED_COUNT)
        return element.text.replace('回', '')

    def text_charged_amount(self):
        element = self._driver.find_element(*self._locator.TEXT_CHARGED_AMOUNT)
        return element.text.replace('円', '').replace(',', '')


class CreditChargeInputPage(BaseMenuPage):
    _locator = CreditChargeInputPageLocators

    def input_amount(self, value):
        element = self._driver.find_element(*self._locator.INPUT_AMOUNT)
        element.send_keys(value)

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeConfirmPage(self._driver)


class CreditChargeConfirmPage(BaseMenuPage):
    _locator = CreditChargeConfirmPageLocators

    def click_back(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK)
        element.click()
        return CreditChargeInputPage(self._driver)

    def click_confirm(self):
        element = self._driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return CreditChargeSucceedPage(self._driver)


class CreditChargeSucceedPage(BaseMenuPage):
    _locator = CreditChargeSucceedPageLocators

    def click_back_to_top(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK_TO_CREDIT_CHARGE_TOP)
        element.click()
        return CreditChargeMainPage(self._driver)


class CreditChargeCancelInputPage(BaseMenuPage):
    _locator = CreditChargeCancelInputPageLocators
    _title = 'nanaco / nanacoクレジットチャージ解約'

    def input_credit_charge_password(self, password):
        element = self._driver.find_element(*self._locator.INPUT_CREDIT_CHARGE_PWD)
        element.send_keys(password)

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return CreditChargeCancelConfirmPage(self._driver)


class CreditChargeCancelConfirmPage(BaseMenuPage):
    _locator = CreditChargeCancelConfirmPageLocators
    _title = 'nanaco / nanacoクレジットチャージ解約確認'

    def click_confirm(self):
        element = self._driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return CreditChargeCancelSucceedPage(self._driver)


class CreditChargeCancelSucceedPage(BaseMenuPage):
    _locator = CreditChargeCancelSucceedPageLocators
    _title = 'nanaco / nanacoクレジットチャージ解約完了'

    def click_back_to_home(self):
        element = self._driver.find_element(*self._locator.BUTTON_BACK_TO_HOME)
        element.click()
        return MenuPage(self._driver)


class CreditChargeErrorPage(BasePage):
    _locator = CreditChargeErrorPageLocators

    def text_alert_msg(self):
        element = self._driver.find_element(*self._locator.ALERT)
        return element.text


class RegisterGiftPage(BasePage):
    _locator = RegisterGiftPageLocators

    def click_next(self):
        element = self._driver.find_element(*self._locator.BUTTON_NEXT)
        element.click()
        return RegisterGiftInputPage(self._driver)


class RegisterGiftInputPage(BasePage):
    _locator = RegisterGiftInputPageLocators

    def input_giftcode(self, code):
        element = self._driver.find_element(*self._locator.INPUT_GIFTCODE_1)
        element.send_keys(code[0:4])

        element = self._driver.find_element(*self._locator.INPUT_GIFTCODE_2)
        element.send_keys(code[4:8])

        element = self._driver.find_element(*self._locator.INPUT_GIFTCODE_3)
        element.send_keys(code[8:12])

        element = self._driver.find_element(*self._locator.INPUT_GIFTCODE_4)
        element.send_keys(code[12:16])

    def click_confirm(self):
        element = self._driver.find_element(*self._locator.BUTTON_CONFIRM)
        element.click()
        return RegisterGiftConfirmPage(self._driver)


class RegisterGiftConfirmPage(BasePage):
    _locator = RegisterGiftConfirmPageLocators

    def text_amount(self):
        element = self._driver.find_element(*self._locator.TEXT_AMOUNT)
        return element.text

    def text_nanaco_number(self):
        element = self._driver.find_element(*self._locator.TEXT_NANACO_NUMBER)
        return element.text

    def text_gift_id(self):
        element = self._driver.find_element(*self._locator.TEXT_GIFT_ID)
        return element.text

    def click_register(self):
        element = self._driver.find_element(*self._locator.BUTTON_REGISTER)
        element.click()
        return RegisterGiftConfirmPage(self._driver)


class RegisterGiftAfterPage(BasePage):
    _locator = RegisterGiftAfterPageLocators
