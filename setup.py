import os
from setuptools import (
    find_packages,
    setup)


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='pubg-python',
    version='0.12.5',
    description='A python wrapper for the PUBG developer API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/ramonsaraiva/pubg-python',
    author='Ramon Saraiva',
    author_email='ramonsaraiva@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests*',)),
    install_requires=[
        'requests>=2.18.4',
        'furl>=1.0.1',
    ],
    extras_require={
        ":python_version<='3.4'": ['enum34>=1.1.6'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
