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

    # Shouldn't affect colours-cli formatting
    assert (
        trans_str("{{3Hi!}} world", {}) == u"{{3Ｈｉ!}}  ｗｏｒｌｄ"
    )


def test_format_str_tags():
    assert (
        trans_str("Hello <world>!", {}) == u"Ｈｅｌｌｏ  <ｗｏｒｌｄ>!"
    )

    assert (
        trans_str("Hello <world>!", {}, tags=True) == u"Ｈｅｌｌｏ  <world>!"
    )
