from setuptools import (
    find_packages,
    setup,
)

FILE_NAME = "VERSION"


def get_version():
    with open(FILE_NAME) as file:
        return file.read()


def get_base_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


def get_long_description():
    with open("README.md", encoding="utf-8") as file:
        return file.read()


setup(
    name="popug_schema_registry",
    version=get_version(),
    package_data={"popug_schema_registry": ["schemas/*.json"]},
    description="Package for uber popug training project schema registry",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Drozdetskiy/popug_jira",
    author="Mikhail Drozdetskiy",
    author_email="m.drozdetskiy.dev@gmail.com",
    packages=find_packages(),
    install_requires=get_base_requirements(),
    include_package_data=True,
    zip_safe=False,
)
