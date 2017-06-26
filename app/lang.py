import json
import os

from settings import LANGUAGE, datadir

langdir = os.path.join(datadir, 'languages')


class Strings(object):
    def __init__(self, lang_file):
        with open(lang_file, 'r') as lang:
            strings = json.load(lang)

            for key, value in strings.items():
                setattr(self, key, value)


s = Strings(os.path.join(langdir, '%s.json' % LANGUAGE))
