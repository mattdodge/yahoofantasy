import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    reqs = f.read().splitlines()

with open("yahoofantasy/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)


setuptools.setup(
    name="yahoofantasy",
    version=version,
    author="Matt Dodge",
    author_email="matt@dodge.com",
    description="An SDK for the Yahoo! Fantasy Sports API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=reqs,
    url="https://github.com/mattdodge/yahoofantasy",
    packages=setuptools.find_packages(),
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        yahoofantasy=yahoofantasy.cli:yahoofantasy
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
