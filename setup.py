from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in sales_addon/__init__.py
from sales_addon import __version__ as version

setup(
	name='sales_addon',
	version=version,
	description='Customize feature of sales module in erpnext',
	author='Raj Tailor',
	author_email='raaj@akhilaminc.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
