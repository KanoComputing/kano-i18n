#!/usr/bin/env python
#
# setup.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from distutils.core import setup

setup(
    name='Kano i18n',
    version='1.0',
    description='i18n tools for Kano OS',
    author='Team Kano',
    author_email='dev@kano.me',
    url='https://github.com/KanoComputing/kano-i18n',
    packages=['kano_i18n'],
    data_files=[('/usr/share/i18n/locales/', ['dev_locale/en_QQ'])]
)
