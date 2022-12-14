"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['./main.py']
OPTIONS = {
    'packages': ['requests', 'selenium', 'pyfiglet', 'pyfiglet.fonts']
}
DATA_FILES=['Get3dsVerification.py','Send_Screenshot.py','Send_Screenshot_Ordercomplete.py','config.ini']

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
