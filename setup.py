from setuptools import setup, find_packages

setup(
    name='oscilloscope_control',
    version='0.1',
    packages=find_packages(),
    py_modules=['oscilloscope_control'],
    install_requires=[
        'numpy',
        'matplotlib',
        'RsInstrument'
    ]
)
