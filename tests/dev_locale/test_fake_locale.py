# coding:utf8

from dev_locale.translate import trans_str


def test_trans_str():
    assert trans_str("Hi", {}) == u"Ｈｉ"
    assert trans_str("Hi %s", {}) == u"Ｈｉ  %s"
