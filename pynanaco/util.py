# -*- coding: utf-8 -*-
import re


def parse_giftcode(text):
    """
    引数の文字列からnanacoギフトコードを抽出する.
    :param text:
    :return:
    """
    return list(set(re.findall('[A-Za-z0-9]{16}', text)) - set(re.findall('NAN[A-Z0-9]{13}', text)))
