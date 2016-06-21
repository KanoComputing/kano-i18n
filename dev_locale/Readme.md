## Fake locale generator

This directory contains
 * A script to generate fake locale data
 * a locale control file to allow apps to display the fake locale

The fake locale is English en the fake region 'QQ'. Hence, apps
should fall back to generic 'en' data if 'en_QQ' is not present.

QQ is a ISO_3166-1 "User assigned code element" which should not clash
with any real country/region code.


To generate locale data for an app:
generate the file `messages.pot` from the soucre code, then run:
`fake_locale messages.pot en_QQ.po` to generate the new po file.

Follow the isntructions in TRANSLATION.md for that app to add the po file.



To use:

copy en_QQ to `/usr/share/i18n/locales/` on the target machine.
Run `sudo dpkg-reconfigure locales`; add and select the 'en_QQ' locale