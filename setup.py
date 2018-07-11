from setuptools import (
    find_packages,
    setup)

setup(
    name='pubg-python',
    version='0.3.3',
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
    extras_require={
        ":python_version<='3.4'": ['enum34>=1.1.6'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
