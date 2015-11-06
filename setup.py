from setuptools import setup, find_packages

setup(
    name='infra_reports',
    version='0.0.0.dev0',
    packages=find_packages(),
    install_requires=[
        'mozci',
    ],
    author='Armen Zambrano G.',
    author_email='armenzg@mozilla.com',
    description="This tool allows generating reports about Mozilla's CI",
    license='MPL',
    url='http://github.com/armenzg/infra_reports',
)
