from codecs import open as copen
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with copen(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyopenload',
    version='0.7',
    description='Python wrapper for openload.co API',
    long_description=long_description,
    url='https://github.com/mohan3d/PyOpenload',
    author='Mohaned Magdy',
    author_email='mohan3d94@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['openload', 'wrapper', 'api', 'api client'],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['requests>=2.20.0', 'requests-toolbelt==0.9.1'],
)
