import base64
import os
import pytest
import __builtin__
from gettext import GNUTranslations, NullTranslations
from test.test_support import EnvironmentVarGuard

import kano_i18n.init
from kano_i18n.init import register_domain, install, get_current_translation


# Test mo file (from cpython test_gettext.py)
GNU_MO_DATA = '''\
3hIElQAAAAAGAAAAHAAAAEwAAAALAAAAfAAAAAAAAACoAAAAFQAAAKkAAAAjAAAAvwAAAKEAAADj
AAAABwAAAIUBAAALAAAAjQEAAEUBAACZAQAAFgAAAN8CAAAeAAAA9gIAAKEAAAAVAwAABQAAALcD
AAAJAAAAvQMAAAEAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABQAAAAYAAAACAAAAAFJh
eW1vbmQgTHV4dXJ5IFlhY2gtdABUaGVyZSBpcyAlcyBmaWxlAFRoZXJlIGFyZSAlcyBmaWxlcwBU
aGlzIG1vZHVsZSBwcm92aWRlcyBpbnRlcm5hdGlvbmFsaXphdGlvbiBhbmQgbG9jYWxpemF0aW9u
CnN1cHBvcnQgZm9yIHlvdXIgUHl0aG9uIHByb2dyYW1zIGJ5IHByb3ZpZGluZyBhbiBpbnRlcmZh
Y2UgdG8gdGhlIEdOVQpnZXR0ZXh0IG1lc3NhZ2UgY2F0YWxvZyBsaWJyYXJ5LgBtdWxsdXNrAG51
ZGdlIG51ZGdlAFByb2plY3QtSWQtVmVyc2lvbjogMi4wClBPLVJldmlzaW9uLURhdGU6IDIwMDAt
MDgtMjkgMTI6MTktMDQ6MDAKTGFzdC1UcmFuc2xhdG9yOiBKLiBEYXZpZCBJYsOhw7FleiA8ai1k
YXZpZEBub29zLmZyPgpMYW5ndWFnZS1UZWFtOiBYWCA8cHl0aG9uLWRldkBweXRob24ub3JnPgpN
SU1FLVZlcnNpb246IDEuMApDb250ZW50LVR5cGU6IHRleHQvcGxhaW47IGNoYXJzZXQ9aXNvLTg4
NTktMQpDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiBub25lCkdlbmVyYXRlZC1CeTogcHlnZXR0
ZXh0LnB5IDEuMQpQbHVyYWwtRm9ybXM6IG5wbHVyYWxzPTI7IHBsdXJhbD1uIT0xOwoAVGhyb2F0
d29iYmxlciBNYW5ncm92ZQBIYXkgJXMgZmljaGVybwBIYXkgJXMgZmljaGVyb3MAR3V2ZiB6YnFo
eXIgY2ViaXZxcmYgdmFncmVhbmd2YmFueXZtbmd2YmEgbmFxIHlicG55dm1uZ3ZiYQpmaGNjYmVn
IHNiZSBsYmhlIENsZ3ViYSBjZWJ0ZW56ZiBvbCBjZWJpdnF2YXQgbmEgdmFncmVzbnByIGdiIGd1
ciBUQUgKdHJnZ3JrZyB6cmZmbnRyIHBuZ255YnQgeXZvZW5lbC4AYmFjb24Ad2luayB3aW5rAA==
'''


@pytest.yield_fixture
def test_env():
    with EnvironmentVarGuard() as env:
        yield env


def setup_function(function):
    # Clear global variables before each test
    kano_i18n.init.REGISTERED_DOMAINS.clear()
    kano_i18n.init.CURRENT_TRANSLATION = None
    kano_i18n.init.DOMAINS_TO_REGISTER = []


def test_register_domain_fallback(tmpdir, test_env):
    test_env['LANG'] = 'en_GB'
    locale_dir = tmpdir.ensure('en_GB', 'LC_MESSAGES', dir=True)

    # setup top level domain (has no translations)
    install('app-domain', locale_dir=tmpdir.strpath)

    domain1_mo = os.path.join(locale_dir.strpath, 'domain-1.mo')
    with open(domain1_mo, 'wb') as fp:
        fp.write(base64.decodestring(GNU_MO_DATA))

    # register a new domain (with translations)
    register_domain('domain-1', locale_dir=tmpdir.strpath)

    # inspect domain setup
    current_translation = get_current_translation()
    assert current_translation is not None
    assert isinstance(current_translation, NullTranslations)
    assert current_translation._fallback is not None
    assert current_translation._fallback._fallback is None
    assert isinstance(current_translation._fallback, GNUTranslations)

    assert _('Hi') == 'Hi'
    assert _('nudge nudge') == 'wink wink'  # Translation comes from domain-1


def test_register_domain_fallback_duplicate():
    """Registering the same domain multiple times should do nothing"""

    install('app-domain')

    current_translation = get_current_translation()
    assert current_translation is not None
    assert current_translation._fallback is None

    register_domain('domain-1')
    assert current_translation._fallback is not None
    assert current_translation._fallback._fallback is None

    # register domain again
    register_domain('domain-1')
    assert current_translation._fallback is not None
    assert current_translation._fallback._fallback is None

    # register different domain
    register_domain('domain-2')
    assert current_translation._fallback is not None
    assert current_translation._fallback._fallback is not None


def test_register_domain_deffered():
    """Registering a domain before install is called should queue it up to be
    registered later"""

    assert get_current_translation() is None

    register_domain('domain-1')
    register_domain('domain-1')
    register_domain('domain-2')
    assert get_current_translation() is None

    install('test-domain')

    current_translation = get_current_translation()
    assert current_translation is not None
    assert current_translation._fallback is not None  # domain-1
    assert current_translation._fallback._fallback is not None  # domain-2
    assert current_translation._fallback._fallback._fallback is None


def test_N__deffered_translation():
    install('app-domain')

    assert 'N_' in __builtin__.__dict__

    translated_string = N_('foo')
    assert isinstance(translated_string, unicode)
