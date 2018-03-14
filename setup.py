from setuptools import (
    find_packages,
    setup)

setup(
    name='pubg-python',
    version='0.1.0',
    description='A python wrapper for the PUBG developer API',
    url='https://github.com/ramonsaraiva/pubg-python',
    author='Ramon Saraiva',
    author_email='ramonsaraiva@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests*',)),
    install_requires=[
        'requests>=2.18.4',
        'furl>=1.0.1',
    ],
)
