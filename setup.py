from setuptools import setup, find_packages

setup(
    name='payroll_calculator',
    version='1.0.0',
    description='Calculate the employees weekly salary.',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Alejandro Perez',
    author_email='alextoni@gmail.com',
    license='proprietary',
    install_requires=['pytest']
)
