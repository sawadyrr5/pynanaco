# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class LoginPageLocators:
    INPUT_NANACO_NUMBER = (By.NAME, 'XCID')
    INPUT_CARD_NUMBER = (By.NAME, 'SECURITY_CD')
    INPUT_LOGIN_PWD = (By.NAME, 'LOGIN_PWD')

    BUTTON_LOGIN_BY_CARD = (By.NAME, 'ACT_ACBS_do_LOGIN2')
    BUTTON_LOGIN_BY_PWD = (By.NAME, 'ACT_ACBS_do_LOGIN1')


class AfterLogoutPageLocators:
    BUTTON_BACK_TO_LOGIN = (By.CSS_SELECTOR, '#contents > div > div:nth-child(3) > a > img')


class BaseMenuPageLocators:
    BUTTON_LOGOUT = (By.CSS_SELECTOR, '#logout > a')


class MenuPageLocators(BaseMenuPageLocators):
    BUTTON_CREDIT_CHARGE = (By.CSS_SELECTOR, '#credit > a')
    TOP_MENU_CREDIT_CHARGE = (By.CSS_SELECTOR, '#memberNavi01 > a')
    TEXT_BALANCE_CARD = (By.CSS_SELECTOR, '#memberInfoFull > div:nth-child(1) > div.moneyBox > div.fRight > p')
    TEXT_BALANCE_CENTER = (By.CSS_SELECTOR, '#memberInfoFull > div:nth-child(2) > div.moneyBox > div.fRight > p')


class CreditChargeGuidePageLocators(BaseMenuPageLocators):
    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_REG_GUIDE_NEXT')


class CreditChargePasswordAuthPageLocators(BaseMenuPageLocators):
    INPUT_CREDIT_CHARGE_PWD = (By.NAME, 'CRDT_CHEG_PWD')
    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_CHRG_PWD_AUTH')


class CreditChargeRegPageLocators(BaseMenuPageLocators):
    BUTTON_AGREE = (By.NAME, 'ACT_ACBS_do_CRDT_REG_AGREE')


class CreditChargeRegInput1PageLocators(BaseMenuPageLocators):
    INPUT_NUMBER_1 = (By.NAME, 'CRDT_CARD_NO_1')
    INPUT_NUMBER_2 = (By.NAME, 'CRDT_CARD_NO_2')
    INPUT_NUMBER_3 = (By.NAME, 'CRDT_CARD_NO_3')
    INPUT_NUMBER_4 = (By.NAME, 'CRDT_CARD_NO_4')
    INPUT_EXPIRE_MONTH = (By.NAME, 'CRDT_CARD_VALID_LMT_MONTH')
    INPUT_EXPIRE_YEAR = (By.NAME, 'CRDT_CARD_VALID_LMT_YEAR')
    INPUT_CODE = (By.NAME, 'CRDT_SECURITY_CD')
    INPUT_PHONE = (By.NAME, 'DEC_TEL_NO')
    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_REG_INPUT1')


class CreditChargeRegInput2PageLocators(BaseMenuPageLocators):
    INPUT_NAME = (By.NAME, 'NAME_KN')
    INPUT_BIRTH_YEAR = (By.NAME, 'BTHD_YEAR')
    INPUT_BIRTH_MONTH = (By.NAME, 'BTHD_MONTH')
    INPUT_BIRTH_DAY = (By.NAME, 'BTHD_DAY')

    INPUT_PWD = (By.NAME, 'CRDT_CHEG_PWD')
    INPUT_PWD_CONF = (By.NAME, 'CRDT_CHEG_PWD_CONF')
    INPUT_EMAIL = (By.NAME, 'REG_EMAIL')
    INPUT_EMAIL_CONF = (By.NAME, 'REG_EMAIL_CONF')
    INPUT_INFO_SEND_FLAG = (By.NAME, 'VAL_INF_SND_FLG')

    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_REG_INPUT2')


class CreditChargeRegConfirmPageLocators(BaseMenuPageLocators):
    BUTTON_CONFIRM = (By.NAME, 'ACT_ACBS_do_CRDT_REG_CONF')


class SecurePageLocators:
    INPUT_SECURE_CODE = (By.NAME, 'Password')
    BUTTON_SEND = (By.ID, 'sendButton')


class CreditChargeRegSucceedPageLocators(BaseMenuPageLocators):
    BUTTON_BACK_TO_HOME = (By.CSS_SELECTOR, '#contents > div.tbl730C > div.footbtnArea > a > img')


class CreditChargeMainPageLocators(BaseMenuPageLocators):
    BUTTON_CHARGE = (By.CSS_SELECTOR, '#charge01 > a')
    BUTTON_HISTORY = (By.CSS_SELECTOR, '#charge02 > a')
    BUTTON_CHANGE_PASSWORD = (By.CSS_SELECTOR, '#charge03 > a')
    BUTTON_CHANGE_CREDIT_CARD = (By.CSS_SELECTOR, '#charge04 > a')
    BUTTON_CANCEL = (By.CSS_SELECTOR, '#hedge > li:nth-child(3) > a')

    TEXT_CREDIT_CARD = (By.CSS_SELECTOR, '#contents > div.pageTitle > p')


class CreditChargeHistoryPageLocators(BaseMenuPageLocators):
    TEXT_CHARGED_COUNT = (By.CSS_SELECTOR, '#wakuDesign > tbody > tr:nth-child(2) > td:nth-child(2)')
    TEXT_CHARGED_AMOUNT = (By.CSS_SELECTOR, '#wakuDesign > tbody > tr:nth-child(2) > td:nth-child(4)')


class CreditChargePasswordChangeInputPageLocators(BaseMenuPageLocators):
    INPUT_OLD_PASSWORD = (By.NAME, 'OLD_CRDT_CHEG_PWD')
    INPUT_NEW_PASSWORD = (By.NAME, 'NEW_CRDT_CHEG_PWD')
    INPUT_NEW_PASSWORD_CONF = (By.NAME, 'NEW_CRDT_CHEG_PWD_CONF')
    BUTTON_CONFIRM = (By.NAME, 'ACT_ACBS_do_CRDT_PWD_CHNG_INPUT')


class CreditChargePasswordChangeSucceedPageLocators(BaseMenuPageLocators):
    BUTTON_BACK_TO_CREDIT_CHARGE_TOP = (By.CSS_SELECTOR, '#contents > div.tbl730C > div.footbtnArea > a > img')


class CreditChargeInputPageLocators(BaseMenuPageLocators):
    INPUT_AMOUNT = (By.NAME, 'AMT')
    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_CHRG_INPUT')


class CreditChargeConfirmPageLocators(BaseMenuPageLocators):
    BUTTON_BACK = (By.CSS_SELECTOR, '#btnArea > div.fLeft.pTop8 > a > img')
    BUTTON_CONFIRM = (By.NAME, 'ACT_ACBS_do_CRDT_CHRG_CONF')


class CreditChargeSucceedPageLocators(BaseMenuPageLocators):
    BUTTON_BACK_TO_CREDIT_CHARGE_TOP = (By.CSS_SELECTOR, '#mainTbl > div > div > a > img')


class CreditChargeCancelInputPageLocators(BaseMenuPageLocators):
    INPUT_CREDIT_CHARGE_PWD = (By.NAME, 'CRDT_CHEG_PWD')
    BUTTON_NEXT = (By.NAME, 'ACT_ACBS_do_CRDT_CNCL_INPUT')


class CreditChargeCancelConfirmPageLocators(BaseMenuPageLocators):
    BUTTON_CONFIRM = (By.NAME, 'ACT_ACBS_do_CRDT_CNCL_CONF')


class CreditChargeCancelSucceedPageLocators(BaseMenuPageLocators):
    BUTTON_BACK_TO_HOME = (By.CSS_SELECTOR, '#meil_edit > div.footbtnArea > a > img')


class CreditChargeErrorPageLocators:
    ALERT = (By.ID, 'systemErrorCord')
