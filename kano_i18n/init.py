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
    # N_() defined globally for deferred translation
    __builtin__.__dict__['N_'] = lambda msg: msg

    gettext.install(app, localedir=locale_dir, unicode=1)
