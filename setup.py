from os import path, name
from subprocess import call
from traceback import print_exc

from setuptools import setup, find_packages
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))


class SystemD(install):
    def run(self):
        super().run()
        try:
            if name == 'posix':
                print('Registering service with systemd...')
                with open(path.join(here, 'minipyp', 'minipyp.service')) as stream:
                    executable = path.join(self.install_scripts, 'minipyp')
                    service = stream.read().format(executable)
                    with open(path.join('lib', 'systemd', 'system', 'minipyp.service'), 'w') as target:
                        target.write(service)
                call(['systemd', 'enable', 'minipyp'])
        except:
            print('Failed to register service. Printing traceback and continuing install...')
            print_exc()


with open(path.join(here, 'README.rst')) as file:
    readme = file.read()
with open(path.join(here, 'HISTORY.rst')) as file:
    readme += '\n\n' + file.read()
there = {}
with open(path.join(here, 'minipyp', 'minipyp.py')) as file:
    exec(file.read(), there)
    if '__version__' not in there.keys():
        raise Exception('Failed to fetch version from source')
setup(
    name='minipyp',
    version=there['__version__'],
    description='A more traditional web server',
    long_description=readme,
    url='https://minipyp.readthedocs.io/en/latest/',
    author='Ryan Garber',
    author_email='ryanmichaelgarber@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Natural Language :: English',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='http https web cgi fast-cgi fpm ssl tls socket proxy reverse',
    packages=find_packages(exclude=['docs', 'tests']),
    download_url='https://github.com/RyanGarber/minipyp/archive/' + there['__version__'] + '.tar.gz',
    install_requires=['requests', 'PyYAML'],
    tests_require=['pytest'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'minipyp=minipyp:main'
        ]
    },
    cmdclass={
        'install': SystemD
    }
)
