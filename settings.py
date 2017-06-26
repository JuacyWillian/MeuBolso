import os

# Directories
appdir = os.path.abspath('.')
datadir = os.path.join(appdir, 'data')
dbdir = os.path.join(datadir, 'database')

# Database
DATABASE_CONFIG = ['sqlite', os.path.join(dbdir, 'storage.db')]
DATABASE_ARGS = {'create_db': True}

# Languages
LANGUAGE = 'pt-br'
TIMEZONE = 'America/Sao_Paulo'

# Fonts
ICONFONTS = [
    {
        'name': 'materialdesign',
        'prefix': 'mdi-',
        'css': os.path.join(datadir, 'fonts', 'materialdesignicons.css'),
        'ttf': os.path.join(datadir, 'fonts', 'materialdesignicons.ttf'),
        'fontd': os.path.join(datadir, 'fonts', 'materialdesignicons.fontd')
    }
]

FONTS = [
    {
        'name': 'ubuntu',
        'fn_regular': os.path.join(datadir, 'fonts', 'Ubuntu-Regular.ttf'),
        'fn_italic': os.path.join(datadir, 'fonts', 'Ubuntu-Italic.ttf'),
        'fn_bold': os.path.join(datadir, 'fonts', 'Ubuntu-Bold.ttf'),
        'fn_bolditalic': os.path.join(datadir, 'fonts', 'Ubuntu-BoldItalic.ttf')
    },
    {
        'name': 'ubuntu light',
        'fn_regular': os.path.join(datadir, 'fonts', 'Ubuntu-Light.ttf'),
        'fn_italic': os.path.join(datadir, 'fonts', 'Ubuntu-LightItalic.ttf'),
    },
    {
        'name': 'ubuntu medium',
        'fn_regular': os.path.join(datadir, 'fonts', 'Ubuntu-Medium.ttf'),
        'fn_italic': os.path.join(datadir, 'fonts', 'Ubuntu-MediumItalic.ttf'),
    },
]
