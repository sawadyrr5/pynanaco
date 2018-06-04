# About this library
Operating nanaco homepage by selenium+python.

## How to install

```py:*.py
pip install git+https://github.com/sawadyrr5/PyNanaco
```

## How to use
### Register new creditcard.

```py:*.py
from pynanaco.core import PyNanaco

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# set personal info
param_p = {
    "name":'john doe',
    "birth_year":'1900',
    "birth_month":'1',
    "birth_day":'1',
    "password":'password',
    "mail":'johndoe@example.com',
    "send_info":'2',
    "phone":'1234567890'
}

# set credit card info
param_c = {
    "number":'1111222233334444',
    "expire_month":'01',
    "expire_year":'22',
    "code":'000',
    "security_code":'abcdefgh'
)

params = {}
params.update(param_p)
params.update(param_c)

# register credit card
nanaco = PyNanaco(**param_n)
nanaco.login()
nanaco.login_credit_charge('password')
nanaco.register(**params)
nanaco.logout()
nanaco.quit()
```

### Charge.

```py:*.py
from pynanaco.core import PyNanaco

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# charge
nanaco = PyNanaco(**param_n)
nanaco.login()
nanaco.login_credit_charge('password')
nanaco.charge(10000)
nanaco.logout()
nanaco.quit()
```

### Cancel credit card.

```py:*.py
from pynanaco.core import PyNanaco

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# cancel credit card
nanaco = PyNanaco(**param_n)
nanaco.login()
nanaco.login_credit_charge('password')
nanaco.cancel('password')
nanaco.logout()
nanaco.quit()
```

### Check info

```py:*.py
from pynanaco.core import PyNanaco

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# get info
nanaco = PyNanaco(**param_n)
nanaco.login()
nanaco.login_credit_charge('password')

print(
    nanaco.registered_creditcard,
    nanaco.balance_card,
    nanaco.balance_center
)

nanaco.logout()
nanaco.quit()

```

## Required

1 - install selenium
```py:*.py
pip install selenium
```

2 - webdriver put into pynanaco/bin.

[chrome webdriver](https://chromedriver.storage.googleapis.com/index.html?path=2.30/)
