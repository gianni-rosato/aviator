from setuptools import setup, find_packages

setup(
    name='rAV1ator',
    version='1.0.0',
    description='AV1/OPUS Encoder GUI',
    author='Nate Sales',
    author_email='nate@natesales.net',
    packages=find_packages(),
    package_data={'': ['window.ui']},
    include_package_data=True,
    classifiers=[],
    install_requires=[],
)
