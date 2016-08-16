# coding:utf8
#
# translate.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Functions and classes to translate strings to wide latin
#

import re

# Code to translate one character to Wide Latin
english_lower = re.compile('[a-z]')
english_upper = re.compile('[A-Z]')

english_lower_wide = u'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
english_upper_wide = u'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'


def trans_char(c):
    if english_lower.match(c):
        return english_lower_wide[ord(c)-ord('a')]
    elif english_upper.match(c):
        return english_upper_wide[ord(c)-ord('A')]
    elif c == ' ':
        return '  '
    else:
        return c


# The following classes are all state machines which identify
# which characters of a string are okay to translate.
# They expect to be fed the string one character at a time.

class DefaultEscape:
    TRANSLATING = 0
    INSIDE_FORMAT_DEFINITION = 1
    SEEN_ESCAPE_CHARACTER = 2

    def __init__(self):
        self.state = self.TRANSLATING

    def okay(self, char):
        """
        Return True if this is a format specifier character
        Eg, the 's' in %s
        """

        if self.state == self.TRANSLATING:
            if char == '%':
                self.state = self.SEEN_ESCAPE_CHARACTER
                return False
            if char == '{':
                self.state = self.INSIDE_FORMAT_DEFINITION
                return False
            return True

        if self.state == self.SEEN_ESCAPE_CHARACTER:
            if char != '%':
                self.state = self.TRANSLATING
                return False

        if self.state == self.INSIDE_FORMAT_DEFINITION:
            if char == ':':
                # end of format definition
                self.state = self.TRANSLATING
            return False

        raise Exception('Invalid state')


class PythonBraceEscape:
    """
    Don't translate char inside  {}, but ignore doubled {{ or }}
    """

    TRANSLATING = 0
    SEEN_OPENING_BRACE = 1
    INSIDE_BRACES = 2
    SEEN_CLOSING_BRACE = 3

    def __init__(self):
        self.state = self.TRANSLATING

        # value of state after parsing char above it:

        # "xxx{fo}}o}yyy"
        #  0001223223000

        # "xxx{{foo}}yyy"
        #  0001000000000

    def okay(self, char):
        """
        Return True if char is part of a python format key
        Eg 'o' in '{foo}'
        """
        if self.state == self.TRANSLATING:
            if char == '{':
                self.state = self.SEEN_OPENING_BRACE
        elif self.state == self.SEEN_OPENING_BRACE:
            if char == '{':
                self.state = self.TRANSLATING
            else:
                self.state = self.INSIDE_BRACES
        elif self.state == self.INSIDE_BRACES:
            if char == '}':
                self.state = self.SEEN_CLOSING_BRACE
        elif self.state == self.SEEN_CLOSING_BRACE:
            if char == '}':
                self.state = self.INSIDE_BRACES
            else:
                self.state = self.TRANSLATING
        return self.state == self.TRANSLATING


class ShEscape:
    TRANSLATING = 0
    DOLLAR_LAST_CHAR = 1
    INSIDE_DOLLAR_NAME = 2
    INSIDE_BRACE_NAME = 3

    def __init__(self):
        """
        Don't translate $variable_name or ${variable_name}
        """
        self.state = self.TRANSLATING

        # value of state after parsing char above it:
        # "xxx$variable,dfff"
        #  00012222222200000

        # "xxx${variable}dff"
        #  00013333333330000

    def okay(self, char):
        """
        Return True if char is part of a shell variable name
        Only care about restriected syntax supported by GNU gettext,
        not every feature of sh:
        $variable_name
        ${variable_name}
        """
        if self.state == self.TRANSLATING:
            if char == '$':
                self.state = self.DOLLAR_LAST_CHAR
        elif self.state == self.DOLLAR_LAST_CHAR:
            if char == '{':
                self.state = self.INSIDE_BRACE_NAME
            else:
                self.state = self.INSIDE_DOLLAR_NAME
        elif self.state == self.INSIDE_DOLLAR_NAME:
            if not (char.isalnum() or char == '_'):
                self.state = self.TRANSLATING
        elif self.state == self.INSIDE_BRACE_NAME:
            if char == '}':
                self.state = self.TRANSLATING
        return self.state == self.TRANSLATING


class TagEscape:
    """
    Don't translate insice '<>'. Also and with any other checker
    """
    def __init__(self, checker):
        self.bracket_count = 0
        self.checker = checker

    def okay(self, char):
        if char == '<':
            self.bracket_count = self.bracket_count + 1
        elif char == '>':
            self.bracket_count = max(self.bracket_count - 1, 0)
        return self.checker.okay(char) and self.bracket_count == 0


def trans_str(msgstr, flags, tags=False):
    """
    Translate a whole string to wide latin, skipping special codes
    """
    out = []

    # We need to avoid translating variable names or format specifiers
    # Decide here how these are delimited based on flags

    if 'sh-format' in flags:
        checker = ShEscape()
    elif 'python-brace-format' in flags:
        checker = PythonBraceEscape()
    else:
        checker = DefaultEscape()

    # For html-like tags
    if tags:
        checker = TagEscape(checker)

    for c in msgstr:
        if checker.okay(c):
            out.append(trans_char(c))
        else:
            out.append(c)

    return u''.join(out)
