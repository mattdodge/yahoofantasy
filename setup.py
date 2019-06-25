import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = [
    'requests',
    'xmljson',
]

setuptools.setup(
    name="yahoofantasy",
    version="0.0.2",
    author="Matt Dodge",
    author_email="matt@dodge.com",
    description="An SDK for the Yahoo! Fantasy Sports API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=reqs,
    url="https://github.com/mattdodge/yahoofantasy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
