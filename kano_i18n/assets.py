# assets.py
#
# Copyright (C) 2018 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Utility function for finding non-text translated assets
#

import locale
import os


def get_path(base, relative, default='en_US'):
    """ Return the path of an asset, either one
        specific to the locale or a default one

        Assets need to be laid out in the following way:
        /base/en_US/relative
        /base/en_AR/relative

        where base is a directory path and relative should
        contain any subdirectory path elements as well as
        the filename.

    Args:
        base (str): The base directory in which i18n asset directories
                    can be found
        relative (str): The relative path (including filename).
        default (str): path element to use in case teh one specific
                       to this locale is missing

    Returns:
        path: the path to the asset.
    """
    (code, encoding) = locale.getdefaultlocale()
    best = os.path.join(base, code, relative)
    if os.path.exists(best):
        return best
    else:
        return os.path.join(base, default, relative)
