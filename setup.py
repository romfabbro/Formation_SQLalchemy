import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

project_name = [ f for f in os.listdir( os.curdir ) if os.path.isdir(f) ][0]

requires = [
    'pyramid',
    'pypyodbc',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'sqlalchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress'
    ]

setup(name=project_name,
    version='0.0',
    description='project_name',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
    "Programming Language :: Python",
    "Framework :: Pyramid",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite=project_name,
    install_requires=requires,
    entry_points="""\
    [paste.app_factory] 
    main = """+project_name+""":main"""
    )

f1 = open('development.ini.default', 'r')
f2 = open('development.ini', 'w')
for line in f1:
    f2.write(line.replace('project_name', project_name))
f1.close()
f2.close()