import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pjkiserver",
	version="0.1.0",
	author="2020 AOT PJKI Course @ TU Berlin",
	author_email="winkels@campus.tu-berlin.de",
	description="Gameserver for the 2020 AOT AI Tournament at TU Berlin",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.tubit.tu-berlin.de/PJ-KI/server",
	packages=[
		"pjkiserver",
		"pjkiserver.ruleserver",
		"pjkiserver.storage",
	],
	install_requires=[
		"flask",
		"numpy",
		"pymongo",
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
