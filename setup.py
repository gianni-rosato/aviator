from setuptools import setup, find_packages

setup(
    name='Aviator',
    version='0.6.4',
    description='AV1/OPUS Encoder GUI',
    author='Gianni Rosato',
    author_email='grosatowork@proton.me',
    packages=find_packages(),
    package_data={'': ['window.ui']},
    include_package_data=True,
    classifiers=[],
    install_requires=[],
)
