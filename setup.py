import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (without reloading it)
with open(join(dirname(__file__), 'bddrest', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'pymlconf >= 0.8.4',
    'webtest'
]


setup(
    name='bddrest',
    version=package_version,
    description='A toolchain for testing REST APIs in BDD.',
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bddrest = restfulpy:main'
        ]
    },
    test_suite='bddrest.tests',
    license='MIT'
)
