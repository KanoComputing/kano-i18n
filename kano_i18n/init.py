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
DOMAINS_TO_REGISTER = []
CURRENT_TRANSLATION = None


def deferred_translation(msg):
    if isinstance(msg, unicode):
        return msg
    return unicode(msg, encoding='utf8')  # Assume original string is utf8 encoded


def install(app, locale_dir=None):
    global CURRENT_TRANSLATION

    # N_() defined globally for deferred translation
    __builtin__.__dict__['N_'] = deferred_translation

    trans = gettext.translation(app, localedir=locale_dir, fallback=True, codeset=None)
    trans.install(True, names=None)

    CURRENT_TRANSLATION = trans

    if len(DOMAINS_TO_REGISTER) > 0:
        for domain in DOMAINS_TO_REGISTER:
            register_domain(*domain)


def register_domain(domain, locale_dir=None):
    """
    Register a domain as a fallback to the currently installed translation.
    If there is no currently installed translation then queue it up to be
    registered when `install` is called.

    Used by library modules to register their translations on top of the current
    app translation.
    """
    global REGISTERED_DOMAINS
    global CURRENT_TRANSLATION
    global DOMAINS_TO_REGISTER

    if not hasattr(__builtin__, '_') or not CURRENT_TRANSLATION:
        # Install hasn't been called yet so defer setup
        DOMAINS_TO_REGISTER.append(
            (domain, locale_dir)
        )
        # and register stubs for _ and N_
        __builtin__.__dict__['_'] = lambda msg: msg
        __builtin__.__dict__['N_'] = lambda msg: msg
        return

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
