
import setuptools

# TODO(niklas9):
# * add more 'classifiers' to get better reach
# * why was 'test_suite' commented out?
# * what's 'include package data' for?
# * what does 'zip_safe" mean?
# * how long can description be? look for inspiration, django etc 

install_requires = ['requests']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')

setuptools.setup(
    name='testvibe',
    version='0.0.1',
    author='Niklas Andersson',
    author_email='nandersson900@gmail.com',
    description=('High-level Python test framework designed for RESTful JSON '
                 'APIs'),
    url='https://github.com/Niklas9/testvibe',
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'nose',
        'coverage'
    ],
    packages=setuptools.find_packages(),
    #test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development'
    ],
)
