# -*- coding: utf-8 -*-
"""Setup file for pip install"""
from pathlib import Path

import setuptools

project_dir = Path(__file__).parent

setuptools.setup(
    name="continuo",
    version="0.2.2",
    description="Procedural music generator",
    long_description=project_dir.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    keywords=["python"],
    author="Richard Baltrusch",
    url="https://github.com/rbaltrusch/continuo",
    packages=setuptools.find_packages("."),
    package_dir={"": "."},
    python_requires=">=3.8",
    include_package_data=True,
    package_data={"continuo": ["py.typed"]}, # for mypy
    # This is a trick to avoid duplicating dependencies between both setup.py and requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    install_requires=project_dir.joinpath("requirements.txt")
    .read_text(encoding="utf-8")
    .split("\n"),
    zip_safe=False,
    license="AGPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Artistic Software",
        "Topic :: Desktop Environment",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Typing :: Typed",
    ],
)
