from distutils.core import setup

## List of tags: http://docs.python.org/distutils/setupscript.html#meta-data

setup(
    name='csvsimple',
    version='0.1.1',
    author='Denis BEURIVE (http://beurive.com/)',
    author_email='denis.beurive@gmail.com',
    py_modules=['csvsimple'],
    scripts=[],
    url='http://pypi.python.org/pypi?name=csvsimple',
    license=open('LICENSE.txt').read(),
    description='Very simple CSV utility for Python 3.',
    long_description=open('README.txt').read(),
    download_url='https://github.com/denis-beurive/csvsimple/zipball/master',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
    ],
)
