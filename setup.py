import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'eventlet',
    'gunicorn',
    'huey',
    'jinja2',
    'peewee',
    'falcon',
    'falcon-autocrud',
    'PasteDeploy',
    'SQLAlchemy',
]

setup(
    name='testrunner',
    version='0.0',
    description='testrunner',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Falcon',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web falcon',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = testrunner:main',
        ],
        'console_scripts': [
            'initialize_testrunner_db = testrunner.scripts.initializedb:main',
        ],
    },
)
