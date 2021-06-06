import os

pwd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(pwd, 'VERSION')) as version_file:
    __version__ = version_file.read().strip()
