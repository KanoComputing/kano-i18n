# coding: utf-8
# test_fake_locale.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Tests for fake_locale script
#

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
