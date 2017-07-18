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

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            self.__setattr__(str(item), str(item))
            return self.__getattr__(item)


s = Strings(os.path.join(langdir, '%s.json' % LANGUAGE))


def gettext(key):
    value = ''
    try:
        value = getattr(s, key)
    except:
        setattr(s, key, key)
        value = gettext(key)
    finally:
        return value
