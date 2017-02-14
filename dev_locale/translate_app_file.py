#!/usr/bin/env python
#
# USAGE: translate_app_file.py file.app file.po
import polib
import sys
import json

app = json.loads(file(sys.argv[1]).read())
po = polib.pofile(sys.argv[2])

to_translate = ['title', 'tagline', 'description']

for key in to_translate:
    if key in app:
        translated = po.find(app[key])
        if translated and translated.msgstr:
            app[key] = translated.msgstr
        else:
            print >>sys.stderr, "Warning : {} not translated".format(app[key])

print json.dumps(app, indent=4)
