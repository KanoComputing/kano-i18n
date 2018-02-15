# assets.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Utility function for finding non-text translated assets
#

import locale
import os


def get_path(base, relative, default='en_US'):
    (code, _) = locale.getdefaultlocale()
    best = os.path.join(base, code, relative)
    if os.path.exists(best):
        return best
    else:
        return os.path.join(base, default, relative)
