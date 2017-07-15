# -*- coding: utf-8 -*-
from time import sleep

import selenium.common
import selenium.webdriver

from pynanaco.page import *


class PyNanaco:
    _home = 'https://www.nanaco-net.jp/pc/emServlet'

    def __init__(self):
        self.driver = selenium.webdriver.Chrome('./chromedriver.exe')
        self.driver.get(self._home)
        self.current_page = LoginPage(self.driver)

        self._nanaco_number = None
        self._card_number = None
        self._credit_charge_password = None
        self._balance_card = None
        self._balance_center = None
        self._registered_credit_card = None
        self._charged_count = None
        self._charged_amount = None

    def is_current(self, page):
        """
        現在のページクラスを取得する
        :param page:
        :return:
        """
        return isinstance(self.current_page, page)

    def login(self, nanaco_number: str, card_number: str = None, password: str = None):
        """
        カード記載の番号またはパスワードでログインする
        :param nanaco_number:
        :param card_number:
        :param password:
        """
        if self.is_current(LoginPage):
            if nanaco_number:
                self.current_page.input_nanaco_number(nanaco_number)
                self._nanaco_number = nanaco_number

            if card_number:
                self.current_page.input_card_number(card_number)
                self.current_page = self.current_page.click_login_by_card()
            elif password:
                self.current_page.input_login_password(password)
                self.current_page = self.current_page.click_login_by_password()

        if self.is_current(MenuPage):
            self._balance_card = self.current_page.text_balance_card()
            self._balance_center = self.current_page.text_balance_center()
            return self._nanaco_number

    def login_credit_charge(self, password: str = None):
        """
        クレジットチャージ画面にログインする.
        :param password:
        :return:
        """
        if self.is_current(MenuPage):
            self.current_page = self.current_page.click_credit_charge()

            # クレジットチャージ未設定の場合はパスワード入力ボックスが出ない
            try:
                self.current_page.input_credit_charge_password(password)
                self.current_page = self.current_page.click_next()
                self._credit_charge_password = password
            except selenium.common.exceptions.NoSuchElementException:
                self.current_page = CreditChargeGuidePage(self.driver)

        if self.is_current(CreditChargeMainPage):
            self._registered_credit_card = self.current_page.text_credit_card()
            return self._registered_credit_card

    def history(self):
        """
        クレジットチャージ実行回数, 金額を取得する.
        :return:
        """
        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_history()

        if self.is_current(CreditChargeHistoryPage):
            self._charged_count = self.current_page.text_charged_count()
            self._charged_amount = self.current_page.text_charged_amount()
            self.driver.back()
            return dict(
                charged_count=self._charged_count,
                charged_amount=self._charged_amount
            )

    def register(self, credit: dict, profile: dict):
        """
        クレジットカードを登録する.
        :param credit:
        :param profile:
        """
        security_code = credit.pop('security_code')

        if self.is_current(CreditChargeGuidePage):
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeRegPage):
            self.current_page = self.current_page.click_agree()

        if self.is_current(CreditChargeRegInput1Page):
            self.current_page.input_credit_card(**credit)
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeRegInput2Page):
            self.current_page.input_profile(**profile)
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeRegConfirmPage):
            self.current_page = self.current_page.click_confirm()

            # PGSE38
            try:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())
            except selenium.common.exceptions.NoSuchElementException:
                sleep(5)

        if self.is_current(SecurePage):
            # PGSE43
            try:
                self.current_page.input_secure_code(security_code)
                self.current_page.click_send()
            except selenium.common.exceptions.NoSuchElementException:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())

        if self.is_current(CreditChargeRegSucceedPage):
            self.current_page.click_back_to_home()

    def charge(self, value):
        """
        クレジットチャージを行う.
        :param value:
        """
        charge = 0
        if value < 5000:
            raise PyNanacoCreditChargeError('5000円以上にしてください.')
        elif value > 50000:
            raise PyNanacoCreditChargeError('50000円以下にしてください.')
        elif value % 1000 != 0:
            raise PyNanacoCreditChargeError('1000円単位にしてください.')

        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_charge()

            # PGSE35
            try:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())
            except selenium.common.exceptions.NoSuchElementException:
                pass

        if self.is_current(CreditChargeInputPage):
            if value >= 35000:
                charge = 30000
            elif 30000 < value < 35000:
                charge = value - 5000
            else:
                charge = value

            self.current_page.input_amount(charge)
            self.current_page = self.current_page.click_next()

            # P30185
            try:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())
            except selenium.common.exceptions.NoSuchElementException:
                pass

        if self.is_current(CreditChargeConfirmPage):
            self.current_page = self.current_page.click_confirm()

            # PGSE22
            try:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())
            except selenium.common.exceptions.NoSuchElementException:
                pass

        if self.is_current(CreditChargeSucceedPage):
            self.current_page = self.current_page.click_back_to_top()

            value = value - charge

            if value > 0:
                self.charge(value)

    def cancel(self):
        """
        設定されているクレジットカードを解除する.
        """
        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_cancel()

        if self.is_current(CreditChargeCancelInputPage):
            self.current_page.input_credit_charge_password(self._credit_charge_password)
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeCancelConfirmPage):
            self.current_page = self.current_page.click_confirm()

        if self.is_current(CreditChargeCancelSucceedPage):
            self.current_page = self.current_page.click_back_to_home()
            return True

    def logout(self):
        """
        ログアウトする.
        :return:
        """
        if self.is_current(BaseMenuPage):
            self.current_page.click_logout()

        if self.is_current(AfterLogoutPage):
            return True

    def quit(self):
        """
        ブラウザを終了する.
        """
        self.driver.quit()

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
        return self._registered_credit_card


class PyNanacoError(Exception):
    pass


class PyNanacoCreditChargeError(PyNanacoError):
    pass
