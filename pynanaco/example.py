# -*- coding: utf-8 -*-
from datetime import datetime

from pynanaco.core import PyNanaco

# set your nanaco card information.
my_nanaco = dict(
    nanaco_number='xxxxxxxxxxxxxxxx',
    card_number='yyyyyyy'
)

# set your credit-card information.
my_card = dict(
    number='xxxxxxxxxxxxxxxx',
    expire_month='mm',
    expire_year='yyyy',
    code='xxx',
    phone='xxxxxxxxxxx'
)

# set your profile.
my_profile = dict(
    name='john doe',
    birthday=datetime(1980, 1, 1),
    password='xxxxxxxx',
    mail='xxx@xxx.xxx',
    send_information='2'
)


def example_charge():
    nanaco = PyNanaco()
    nanaco.login_by_card(**my_nanaco)
    nanaco.login_credit_charge('set_credit_charge_password_here')
    nanaco.charge(10000)


def example_set():
    nanaco = PyNanaco()
    nanaco.login_by_card(**my_nanaco)
    nanaco.login_credit_charge(None)
    nanaco.set(
        credit=my_card,
        profile=my_profile,
        secure='set_secure_password_here'
    )


def example_cancel():
    nanaco = PyNanaco()
    nanaco.login_by_card(**my_nanaco)
    nanaco.login_credit_charge('set_credit_charge_password_here')
    nanaco.cancel()


if __name__ == '__main__':
    example_charge()
    example_set()
    example_cancel()
