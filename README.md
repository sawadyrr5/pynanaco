# このライブラリについて
電子マネーnanacoへのクレジットカード登録, クレジットチャージ実行, クレジットチャージ解約, ギフト登録を行います.


## 開発環境
Windows 10 Home

Python 3.5.0

selenium 3.11.0

## インストール方法

```py:*.py
pip install git+https://github.com/sawadyrr5/PyNanaco
```

chromewebdriverが必要です

## 使用方法
### クレジットカードを登録する

```py:*.py
from pynanaco.core import PyNanaco

# set webdriver path
CHROME_PATH = "C:\hoge\chromedriver.exe"

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
nanaco = PyNanaco(CHROME_PATH)
nanaco.login(**param_n)
nanaco.login_credit_charge('password')
nanaco.register(**params)
nanaco.logout()
nanaco.quit()
```

### チャージする

```py:*.py
from pynanaco.core import PyNanaco

# set webdriver path
CHROME_PATH = "C:\hoge\chromedriver.exe"

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# charge
nanaco = PyNanaco(CHROME_PATH)
nanaco.login(**param_n)
nanaco.login_credit_charge('password')
nanaco.charge(10000)
nanaco.logout()
nanaco.quit()
```

### クレジットチャージを解除する

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

### 情報を取得する

```py:*.py
from pynanaco.core import PyNanaco

# set webdriver path
CHROME_PATH = "C:\hoge\chromedriver.exe"

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# get info
nanaco = PyNanaco(CHROME_PATH)
nanaco.login(**param_n)
nanaco.login_credit_charge('password')

print(
    nanaco.registered_creditcard,
    nanaco.balance_card,
    nanaco.balance_center
)

nanaco.logout()
nanaco.quit()

```

### ギフトコードを登録する

```py:*.py
from pynanaco.core import PyNanaco

# set webdriver path
CHROME_PATH = "C:\hoge\chromedriver.exe"

# set nanaco number
param_n = {
    "nanaco_number":'7600000012345678',
    "card_number":'1234567'
    }

# set gift code
code='xxxxxxxxxxxxxxxx'

# get info
nanaco = PyNanaco(CHROME_PATH)
nanaco.login(**param_n)
nanaco.register_giftcode(code)
nanaco.logout()
nanaco.quit()

```

## 開発履歴

0.2.0 ギフトコード登録をサポート

0.1.0 公開
