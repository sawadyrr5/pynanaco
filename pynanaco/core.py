# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pynanaco.page import *

from time import sleep

import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)


class PyNanaco:
    _HOME = 'https://www.nanaco-net.jp/pc/emServlet'

    def __init__(self, file_path, headless=False):

        options = webdriver.ChromeOptions()

        # headlessで動かすために必要なオプション
        if headless:
            options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1280x1696")
        # options.add_argument("--disable-application-cache")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--hide-scrollbars")
        # options.add_argument("--enable-logging")
        # options.add_argument("--log-level=0")
        # options.add_argument("--v=99")
        # options.add_argument("--single-process")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--homedir=/tmp")

        self._driver = webdriver.Chrome(executable_path=file_path, chrome_options=options)
        self._driver.get(self._HOME)

        self.current_page = None

        self._nanaco_number = None
        self._card_number = None
        self._password = None

        self._credit_charge_password = None
        self._balance_card = None
        self._balance_center = None
        self._registered_creditcard = None
        self._charged_count = None
        self._charged_amount = None

    @property
    def balance_card(self):
        return self._balance_card

    @property
    def balance_center(self):
        return self._balance_center

    @property
    def registered_creditcard(self):
        return self._registered_creditcard

    @property
    def charged_count(self):
        return self._charged_count

    @property
    def charged_amount(self):
        return self._charged_amount

    def is_current(self, page):
        """
        Get current page class.
        :param page:
        :return:
        """
        return isinstance(self.current_page, page)

    def login(self, nanaco_number, card_number=None, password=None):
        """
        Login by card number or password.
        """
        self._nanaco_number = nanaco_number
        self._card_number = card_number
        self._password = password

        self.current_page = LoginPage(self._driver)

        if self.is_current(LoginPage):
            if self._nanaco_number and self._card_number:
                self.current_page = self._login_by_number()

            elif self._nanaco_number and self._password:
                self.current_page = self._login_by_password()

        logger.info("login")

        if self.is_current(MenuPage):
            self._balance_card = self.current_page.text_balance_card()
            self._balance_center = self.current_page.text_balance_center()

            logger.info("balance card " + str(self._balance_card))
            logger.info("balance center " + str(self._balance_center))

    def _login_by_number(self):
        """
        :return: MenuPage
        """
        self.current_page.input_nanaco_number(self._nanaco_number)
        self.current_page.input_card_number(self._card_number)

        return self.current_page.click_login_by_card()

    def _login_by_password(self):
        """
        :return: MenuPage
        """
        self.current_page.input_nanaco_number(self._nanaco_number)
        self.current_page.input_login_password(self._password)

        return self.current_page.click_login_by_password()

    def login_credit_charge(self, password: str):
        """
        Login credit charge menu.
        :param password:
        """
        if self.is_current(MenuPage):
            self.current_page = MenuPage(self._driver)
            self.current_page = self.current_page.click_credit_charge()

            # PGSE12
            # 午前4時～5時の間は、システムメンテナンスの為クレジットチャージサービスをご利用いただけません。
            try:
                page = CreditChargeErrorPage(self._driver)
                msg = page.text_alert_msg()

                raise PGSE12Error(msg)
                raise PyNanacoCreditChargeError(msg)

            except NoSuchElementException:
                pass

            # クレジットチャージ未設定の場合はパスワード入力ボックスが出ない
            try:
                self.current_page = CreditChargePasswordAuthPage(self._driver)
                self.current_page.input_credit_charge_password(password)
                self.current_page = self.current_page.click_next()

                logger.info("credit card is registered.")

            except NoSuchElementException:
                self.current_page = CreditChargeGuidePage(self._driver)

                logger.info("credit card is not registered.")

            # 登録済みクレジットカード情報を取得
            if self.is_current(CreditChargeMainPage):
                self._registered_creditcard = self.current_page.text_credit_card()

                logger.info("registered credit card " + self._registered_creditcard)

                self.current_page = self.current_page.click_history()

            # チャージ累計回数と累計金額を取得
            if self.is_current(CreditChargeHistoryPage):
                self._charged_count = self.current_page.text_charged_count()
                self._charged_amount = self.current_page.text_charged_amount()

                logger.info("charged count " + self._charged_count)
                logger.info("charged amount " + self._charged_amount)

                self.current_page = CreditChargeMainPage(self._driver)
                self._driver.back()

    def register(self,
                 number: str, expire_month: str, expire_year: str, code: str, phone: str,
                 name: str, birth_year: str, birth_month: str, birth_day: str, password: str, mail: str, send_info: str,
                 security_code: str
                 ):
        """
        Register credit card.
        :param number: 
        :param expire_month: 
        :param expire_year: 
        :param code: 
        :param phone: 
        :param name: 
        :param birth_year: 
        :param birth_month: 
        :param birth_day: 
        :param password: 
        :param mail: 
        :param send_info: 
        :param security_code: 
        """
        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_credit_charge()

        if self.is_current(CreditChargeGuidePage):
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeRegPage):
            self.current_page = self.current_page.click_agree()

        self._register_1(number, expire_month, expire_year, code, phone)
        self._register_2(name, birth_year, birth_month, birth_day, password, mail, send_info)

        sleep(3)

        self._register_secure(security_code)

        sleep(5)

    def _register_1(self, number: str, expire_month: str, expire_year: str, code: str, phone: str):
        if self.is_current(CreditChargeRegInput1Page):
            self.current_page.input_credit_card(
                number=number,
                expire_month=expire_month,
                expire_year=expire_year,
                code=code
            )
            self.current_page.input_phone(phone=phone)
            self.current_page = self.current_page.click_next()

            logger.info("input credit card #" + number)

    def _register_2(self, name: str, birth_year: str, birth_month: str, birth_day: str, password: str, mail: str,
                    send_info: str):
        if self.is_current(CreditChargeRegInput2Page):
            self.current_page.input_profile(
                name=name,
                birth_year=birth_year,
                birth_month=birth_month,
                birth_day=birth_day,
                password=password,
                mail=mail,
                send_info=send_info
            )
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeRegConfirmPage):
            self.current_page = self.current_page.click_confirm()

    def _register_secure(self, security_code: str):
        if self.is_current(SecurePage):
            self.current_page.input_secure_code(security_code)

            logger.info("input security code " + security_code)

            # if not self._debug_mode:
            self.current_page.click_send()

            logger.info("click send")

        if self.is_current(CreditChargeRegSucceedPage):
            self.current_page.click_back_to_home()

    def charge(self, value: int):
        """
        Charge by creadit card.
        :param value:
        """
        if self.is_current(CreditChargeMainPage):

            self.current_page = self.current_page.click_charge()
            try:
                self._error_handler()

            except:
                pass

            # PGSE35
            try:
                page = CreditChargeErrorPage(self._driver)
                raise PyNanacoCreditChargeError(page.text_alert_msg())

            except NoSuchElementException:
                pass

        if self.is_current(CreditChargeInputPage):
            self.current_page.input_amount(value)
            self.current_page = self.current_page.click_next()

            # P30185
            try:
                page = CreditChargeErrorPage(self._driver)
                raise PyNanacoCreditChargeError(page.text_alert_msg())

            except NoSuchElementException:
                pass

        if self.is_current(CreditChargeConfirmPage):
            self.current_page = self.current_page.click_confirm()

            # PGSE22
            try:
                page = CreditChargeErrorPage(self._driver)
                raise PyNanacoCreditChargeError(page.text_alert_msg())

            except NoSuchElementException:
                pass

        if self.is_current(CreditChargeSucceedPage):
            self.current_page = self.current_page.click_back_to_top()

    def cancel(self, password: str):
        """
        Cancel registered credit card.
        """
        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_cancel()

        if self.is_current(CreditChargeCancelInputPage):
            self.current_page.input_credit_charge_password(password)
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeCancelConfirmPage):
            self.current_page = self.current_page.click_confirm()

            logger.info("cancel succeed")

        if self.is_current(CreditChargeCancelSucceedPage):
            self.current_page = self.current_page.click_back_to_home()

    def register_giftcode(self, code):
        """
        Register giftcode.
        """
        if self.is_current(MenuPage):
            # self.current_page = MenuPage
            self.current_page = self.current_page.click_register_gift()

            self.current_page = self.current_page.click_next()

            whandles = self._driver.window_handles
            self._driver.switch_to.window(whandles[1])

            sleep(2)

            self.current_page.input_giftcode(code)
            self.current_page = self.current_page.click_confirm()

            # コード誤入力
            try:
                logger.info("gift amount       : " + self.current_page.text_amount())
                logger.info("gift nanaco number: " + self.current_page.text_nanaco_number())
                logger.info("gift id           : " + self.current_page.text_gift_id())
                self.current_page = self.current_page.click_register()

            except NoSuchElementException:
                logger.error("gift code error   : " + code)

    def logout(self):
        """
        Logout.
        """
        if self.is_current(BaseMenuPage):
            self.current_page.click_logout()

        if self.is_current(AfterLogoutPage):
            logger.info("logout.")

    def quit(self):
        """
        Quit browser.
        """
        self._driver.quit()

        logger.info("quit.")

    # TODO:
    def _error_handler(self):
        errors = {
            "PGSE05": PGSE05Error,
            "PGSE11": PGSE11Error,
            "PGSE12": PGSE12Error,
            "PGSE15": PGSE15Error,
            "PGSE22": PGSE22Error,
            "PGSE29": PGSE29Error,
            "PGSE35": PGSE35Error,
            "PGSE37": PGSE37Error
        }

        page = CreditChargeErrorPage(self._driver)

        for k, v in errors.items():
            if page.text_alert_msg() in k:
                raise v

    @property
    def nanaco_number(self):
        return self._nanaco_number

    @property
    def card_number(self):
        return self._card_number

    @property
    def balance_card(self):
        return self._balance_card

    @property
    def balance_center(self):
        return self._balance_center

    @property
    def credit_card(self):
        return self._registered_creditcard


class PyNanacoError(Exception):
    def __init__(self, *args):
        self.value = args[0]
        logger.error(self.value)

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        print(__doc__)


class PyNanacoCreditChargeError(PyNanacoError):
    pass


class PGSE05Error(PyNanacoError):
    """
    nanacoの発行・再発行直後のため、nanacoのお申込み時にご記入いただいた情報の登録が完了しておりません。
    そのため、nanacoクレジットチャージお申込み、登録クレジットカード情報設定変更、
    クレジットチャージパスワード再設定ができません。
    恐れ入りますが、カードの場合は入会から10日後、モバイルの場合は入会・機種変更から4日後に
    クレジットチャージ申し込み等を行っていただくようお願いいたします。
    """


class PGSE09Error(PyNanacoError):
    """
    クレジットカード番号および有効期限をご確認の上、再度ご入力ください。
    ご不明な場合は各クレジットカード会社にお問い合せください。
    """


class PGSE11Error(PyNanacoError):
    """
    ご希望のチャージ金額は、チャージ可能限度額を超えています。
    """


class PGSE12Error(PyNanacoError):
    """
    午前4時～5時の間は、システムメンテナンスの為クレジットチャージサービスをご利用いただけません。
    """


class PGSE15Error(PyNanacoError):
    """
    本日のチャージ実行回数が１日の限度回数に達しています。
    """
    pass


class PGSE22Error(PyNanacoError):
    """
    ご指定のクレジットカードは現在ご利用になれません。ご不明な場合は各クレジットカード会社にお問合せ下さい。
    """


class PGSE29Error(PyNanacoError):
    """
    センターお預り分マネーが限度額を超えています。
    クレジットチャージを行うには、センターお預り分マネーをお受け取りください。
    """


class PGSE35Error(PyNanacoError):
    pass


class PGSE37Error(PyNanacoError):
    """
    ・クレジットカード番号および有効期限をご確認のうえ、再度ご入力ください。
    ・クレジットカード番号および有効期限に間違いがない場合、
    本人認証サービス（J/Secure、Verified by VISA、MasterCard SecureCode）未登録の可能性がございます。
    本人認証サービスご登録後にご利用ください。本人認証サービスへのご登録方法がご不明の場合は、
    ご利用のクレジットカード発行会社へお問合せください。
    """
