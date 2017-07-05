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
        self.credit_charge_password = ''

    def is_current(self, page):
        return isinstance(self.current_page, page)

    def login_by_card(self, nanaco_number, card_number):
        if self.is_current(LoginPage):
            self.current_page.input_nanaco_number(nanaco_number)
            self.current_page.input_card_number(card_number)
            self.current_page = self.current_page.click_login_by_card()

    def login_credit_charge(self, password: str = None):
        if self.is_current(MenuPage):
            self.current_page = self.current_page.click_credit_charge()

            # クレジットチャージ未設定の場合はパスワード入力ボックスが出ない
            try:
                self.current_page.input_credit_charge_password(password)
                self.current_page = self.current_page.click_next()
                self.credit_charge_password = password
            except selenium.common.exceptions.NoSuchElementException:
                self.current_page = CreditChargeGuidePage(self.driver)

    def set(self, credit, profile, secure):
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
                self.current_page.input_secure_code(secure)
                self.current_page.click_send()
            except selenium.common.exceptions.NoSuchElementException:
                page = CreditChargeErrorPage(self.driver)
                raise PyNanacoCreditChargeError(page.get_alert_msg())

        if self.is_current(CreditChargeRegSucceedPage):
            self.current_page.click_back_to_home()

    def charge(self, value):
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

        if self.is_current(CreditChargeSucceedPage):
            self.current_page = self.current_page.click_back_to_top()

            value = value - charge

            if value > 0:
                self.charge(value)

    def cancel(self):
        if self.is_current(CreditChargeMainPage):
            self.current_page = self.current_page.click_cancel()

        if self.is_current(CreditChargeCancelInputPage):
            self.current_page.input_credit_charge_password(self.credit_charge_password)
            self.current_page = self.current_page.click_next()

        if self.is_current(CreditChargeCancelConfirmPage):
            self.current_page = self.current_page.click_confirm()

        if self.is_current(CreditChargeCancelSucceedPage):
            self.current_page = self.current_page.click_back_to_home()

    def logout(self):
        if self.is_current(BaseMenuPage):
            self.current_page.click_logout()

    def quit(self):
        self.driver.quit()


class PyNanacoError(Exception):
    pass


class PyNanacoCreditChargeError(PyNanacoError):
    pass
