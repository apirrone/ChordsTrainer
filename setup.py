from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ChordsTrainer",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=["pygame==2.5.2", "mido[ports-rtmidi]==1.3.2"],
    entry_points={
        "console_scripts": [
            "chords-trainer = chordstrainer:main",
        ]
    },
    author="Antoine Pirrone",
    author_email="antoine.pirrone@gmail.com",
    url="https://github.com/apirrone/ChordsTrainer",
    description="TODO",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
