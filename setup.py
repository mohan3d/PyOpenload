from distutils.core import setup

setup(
    name='pyopenload',
    version='0.3',
    packages=['openload'],
    url='https://github.com/mohan3d/PyOpenload',
    license='MIT',
    author='Mohaned Magdy',
    author_email='mohan3d94@gmail.com',
    download_url = 'https://github.com/mohan3d/PyOpenload/tarball/0.3',
    install_requires=[
        'requests',
    ],
    keywords = ['openload', 'wrapper', 'api wrapper'],
    description='Just a python wrapper for openload.co API',
)
