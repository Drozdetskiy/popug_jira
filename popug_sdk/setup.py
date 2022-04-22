from setuptools import (
    find_packages,
    setup,
)

FILE_NAME = "VERSION"


with open(FILE_NAME) as file:
    version = file.read()

with open("requirements.txt") as file:
    requirements = file.readlines()

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="popug_sdk",
    version=version,
    description="Package for uber popug training project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drozdetskiy/popug_jira",
    author="Mikhail Drozdetskiy",
    author_email="m.drozdetskiy@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
