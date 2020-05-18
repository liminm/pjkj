from setuptools import setup

setup(
  name="pjki-server",
  version="0.1.0",
  author="2020 AOT PJKI Course @ TU Berlin",
  author_email="winkels@campus.tu-berlin.de",
  packages=["pjki-server"],
  url="https://gitlab.tubit.tu-berlin.de/PJ-KI/server",
  description="Gameserver for the 2020 AOT AI Tournament at TU Berlin",
  install_requires=[
    "flask",
  ]
)
