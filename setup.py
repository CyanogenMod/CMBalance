import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', 'WebError', 'SQLAlchemy', 'nose', 'pyramid_beaker', 'zope.sqlalchemy']

setup(name='CMBalance',
      version='0.14',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="nose.collector",
      entry_points="""\
      [paste.app_factory]
      main = cmbalance:main
      """,
      paster_plugins=['pyramid'],
      )

