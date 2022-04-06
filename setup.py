from setuptools import setup

setup(
    name='Ploos',
    version='0.1.0',    
    description='Python utilities for VASP files post-processing',
    url='https://github.com/loopoopool/ploos',
    author='Lorenzo Celiberti',
    author_email='lorenzo.celiberti@protonmail.com',
    license='BSD 2-clause',
    packages=['ploos'],
    install_requires=['matplotlib==3.4.3',
                      'numpy',                     
                      'PyQt5'],
)
