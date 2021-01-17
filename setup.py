from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NewsAgent",
    version="1.0",
    author="Allen",
    author_email="allen.haha@hotmail.com",
    description="A News Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Boost Software License Version 1.0",
        "Operating System :: OS Independent",
    ]
)
