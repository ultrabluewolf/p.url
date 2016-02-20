from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#   long_description = f.read()

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

long_description = read_md('README.md')

setup(
  name='p.url',
  version='0.1.0a3',

  description='A simple url parsing library for python',
  long_description=long_description,
  url='https://github.com/ultrabluewolf/p.url',
  author='Britney L.',

  license='MIT',

  classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
  ],

  keywords='url',

  packages=['purl'],

  install_requires=['future>=0.15,<1', 'six>=1.10,<2'],

  extras_require={
    'test': ['pytest']
  }
)