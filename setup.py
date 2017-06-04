#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
	name='sniffMyPackets',
	author='catalyst256',
	version='1.0',
	author_email='catalyst256@gmail.com',
	description='A collection of local transforms relating to packets',
	license='GPL',
	packages=find_packages('src'),
	package_dir={'': 'src'},
	zip_safe=False,
	package_data={
		'': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']  # list of resources
	},
	install_requires=[
		'canari>=1.1',
		'pygeoip>=0.2.6',
		'python-graph-core>=1.8.2',
		'pyxdg>=0.19'
	],
	dependency_links=[
		# custom links for the install_requires
	]
)
