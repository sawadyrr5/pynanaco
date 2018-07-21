import re


def parse_giftcode(text):
    return list(set(re.findall('[A-Za-z0-9]{16}', text)) - set(re.findall('NAN[A-Z0-9]{13}', text)))
