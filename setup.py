from distutils.core import setup

setup(
    name='pyopenload',
    version='0.1dev',
    packages=['src'],
    url='https://github.com/mohan3d/PyOpenload',
    license='MIT',
    author='Mohaned Magdy',
    author_email='mohan3d94@gmail.com',
    install_requires=[
        'requests',
    ],
    description='Just a python wrapper for openload.co API',
    long_description=open('README.md').read(),
)
