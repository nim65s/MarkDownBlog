import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='MarkDownBlog',
    version='2.0.0a',
    packages=['dmdb', 'smdb', 'mdb_settings'],
    install_requires=[
        'markdown',
        'Pygments',
    ],
    extras_require={
        'dmdb': [
            'Django',
            'django-autoslug',
            'django-bootstrap3',
        ],
        'smdb': [
            'jinja2',
            'PyYAML',
        ],
    },
    scripts=['bin/smdb'],
    include_package_data=True,
    license='GPL License',
    description='A simple Django app to blog with markdown.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://saurel.me/',
    author='Guilhem Saurel',
    author_email='webmaster@saurel.me',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
