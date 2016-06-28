# init.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Initialisation utilities for i18n
#

import gettext
import __builtin__


def install(app, locale_dir=None):
    if '_' in __builtin__.__dict__:
        raise Exception("Attempt to install gettext twice")

    # N_() defined globally for deferred translation
    __builtin__.__dict__['N_'] = lambda msg: msg

    gettext.install(app, localedir=locale_dir, unicode=1)


def library_install(module_domain, locale_dir=None):
    """
    Perform bindings for gettext use in shared libraries

    """

    if locale_dir:
        gettext.bindtextdomain(module_domain, locale_dir)
    gettext.bind_textdomain_codeset(module_domain, 'UTF-8')
