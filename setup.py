import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
        name='MarkDownBlog',
        version='0.1.2',
        packages=['dmdb'],
        install_requires=[
            'Django',
            'django-bootstrap3',
            ],
        include_package_data=True,
        license='GPL License',
        description='A simple Django app to blog with markdown.',
        long_description=README,
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
