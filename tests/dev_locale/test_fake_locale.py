# coding:utf8

from dev_locale.translate import trans_str


def test_trans_str():
    assert trans_str("Hi", {}) == u"Ｈｉ"
    assert trans_str("Hi %s %d", {}) == u"Ｈｉ  %s  %d"


def test_custom_format_str():
    """
    Test that the custom formatting syntax used in terminal quest doesn't get
    translated.
    """
    assert (
        trans_str("{{gb:Hi %s!}}", {}) == u"{{gb:Ｈｉ  %s!}}"
    )
