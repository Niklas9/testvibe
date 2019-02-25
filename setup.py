
import setuptools

import testvibe


install_requires = ['colored==1.3.93', 'requests==2.21.0', 'tabulate==0.8.3',
                    'tqdm==4.31.1']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')  # Python 2.6 compatibility

setuptools.setup(
    name='testvibe',
    version=testvibe.VERSION,
    author='Niklas Andersson',
    author_email='nandersson900@gmail.com',
    description=('A high-level Python test framework designed for '
                 'RESTful JSON APIs'),
    license='LGPL',
    url='https://github.com/Niklas9/testvibe',
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'nose==1.3.4',
        'coverage==4.0.3'
    ],
    packages=['testvibe', 'testvibe/core', 'testvibe/project_template'],
    include_package_data=True,
    scripts=['testvibe/tvctl'],
    classifiers=[
        'Development Status :: 3 - Alpha'
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python'
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.6'
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.4'
        'Programming Language :: Python :: 3.5'
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X'
    ],
)
