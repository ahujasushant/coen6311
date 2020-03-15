from setuptools import setup

setup(
    name='coen_6311',
    packages=['coen_6311'],
    include_package_data=True,
    install_requires=[
        'flask==1.1.1',
        'Flask-WTF==0.14.3',
    ],
)