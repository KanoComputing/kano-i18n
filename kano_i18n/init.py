# init.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Initialisation utilities for i18n
#

import gettext
import __builtin__

REGISTERED_DOMAINS = set()
CURRENT_TRANSLATION = None


def install(app, locale_dir=None):
    global CURRENT_TRANSLATION

    # N_() defined globally for deferred translation
    __builtin__.__dict__['N_'] = lambda msg: msg

    trans = gettext.translation(app, localedir=locale_dir, fallback=True, codeset=None)
    trans.install(True, names=None)

    CURRENT_TRANSLATION = trans


def register_domain(domain, locale_dir=None):
    """
    Register a domain as a fallback to the currently installed translation.
    Used by library modules to register their translations on top of the current
    app translation.
    """
    global REGISTERED_DOMAINS
    global CURRENT_TRANSLATION

    if not hasattr(__builtin__, '_'):
        # TODO
        raise Exception('Localization has not been setup')

    if domain in REGISTERED_DOMAINS:
        # Already setup so we bail early here
        return

    # Create translation
    trans = gettext.translation(
        domain,
        localedir=locale_dir,
        fallback=True  # don't throw an error if the no .mo files found for domain, just return `NullTranslations`
    )

    CURRENT_TRANSLATION.add_fallback(trans)
    REGISTERED_DOMAINS.add(domain)


def get_current_translation():
    global CURRENT_TRANSLATION
    return CURRENT_TRANSLATION
