from setuptools import find_packages, setup

SRC = 'src'
name = 'aptscraper'

setup(
    name=name,
    version='0.1.0',
    author='Selim Belhaouane',
    author_email='selim.belhaouane@gmail.com',
    packages=find_packages(SRC),
    package_dir={'': SRC},
    install_requires=[
        'bs4',
        # 'lxml',
        'requests',
        'jsonschema',
    ],
    entry_points={
        'console_scripts': [
            'aptscraper = aptscraper.__main__:cli'
        ]
    },
)
