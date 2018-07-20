import re


def parse_giftcode(text):
    matches = re.findall('[A-Za-z0-9_]{16}', text)
    return [t for t in matches if not 'NAN' in t and not '_' in t]
