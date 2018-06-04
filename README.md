# About this library
Operating nanaco homepage by selenium+python.

## How to install

```
pip install git+https://github.com/sawadyrr5/PyNanaco
```

## How to use


```python:
from pynanaco.core import PyNanaco

param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

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

nanaco = PyNanaco(**param_n)
nanaco.login()
nanaco.login_credit_charge('password')
nanaco.register(**params)
nanaco.logout()
nanaco.quit()
```

[pythonでnanacoクレジットチャージできるモジュールPyNanacoを作った](http://qiita.com/sawadybomb/items/ff3c8283ae80165e7b25)

## Required

1 - install selenium
```
pip install selenium
```

2 - webdriver put into pynanaco/bin.

[chrome webdriver](https://chromedriver.storage.googleapis.com/index.html?path=2.30/)
