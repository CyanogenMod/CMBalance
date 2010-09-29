from setuptools import setup, find_packages
#from src.trumerca.model import __version__

__version__ = "1.0.1"

setup(
      name="CMBalanceClient",
      description="A python client for the CMBalance server.",
      long_description="",
      version=__version__,

      classifiers=[],
      keywords="",
      author="Chris Soyars",
      author_email="ctso@ctso.me",
      url="http://www.github.com/ctso/CMBalance",
      license="",

      packages=find_packages('python'),
      package_dir={"":"python"},

      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points={
          'console_scripts': [
              'cmbalance = cmbalance.shell:main',
          ],
      },
      test_suite="nose.collector",
)
