#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from distutils.core import setup

data_files=[('share/slidessorter', ['data/slidessorter.ui']),
            ('share/applications', ['data/slidessorter.desktop']),
            ('share/man/man1', ['doc/slidessorter.1']),
            ('share/pixmaps', ['data/slidessorter.png']),
            ('share/slidessorter/icons/hicolor/scalable',
                ['data/slidessorter.svg']) ]


# Freshly generate .mo from .po, add to data_files:
if os.path.isdir('mo/'):
    os.system ('rm -r mo/')
for name in os.listdir('po'):
    m = re.match(r'(.+)\.po$', name)
    if m != None:
        lang = m.group(1)
        out_dir = 'mo/%s/LC_MESSAGES' % lang
        out_name = os.path.join(out_dir, 'slidessorter.mo')
        install_dir = 'share/locale/%s/LC_MESSAGES/' % lang
        os.makedirs(out_dir)
        os.system('msgfmt -o %s po/%s' % (out_name, name))
        data_files.append((install_dir, [out_name]))

setup(name='slidessorter',
      version='0.1.0',
      author='Séverin Lemaignan, Konstantinos Poulios',
      author_email='severin@guakamole.org',
      description='Latex Beamer slides sorting and shuffling made easy',
      url = 'https://github.com/severin-lemaignan/slidessorter',
      license='GNU GPL-3',
      scripts=['bin/slidessorter'],
      packages=['slidessorter'],
      data_files=data_files
     )

# Clean up temporary files
if os.path.isdir('mo/'):
    os.system ('rm -r mo/')
if os.path.isdir('build/'):
    os.system ('rm -r build/')

