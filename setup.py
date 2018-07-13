import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (without loading it)
with open(join(dirname(__file__), 'bddrest', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S)\
        .match(v_file.read()).group(1)


dependencies = [
    'webtest',
    'pyyaml',
    'argcomplete'
]


setup(
    name='bddrest',
    version=package_version,
    description='A toolchain for testing REST APIs in BDD manner.',
    long_description=open('README.md').read(),
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bddrest = bddrest.cli:main'
        ]
    },
    test_suite='bddrest.tests',
    license='MIT',
    url='https://github.com/Carrene/bddrest',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]

)
