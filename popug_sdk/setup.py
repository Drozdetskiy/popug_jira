from setuptools import (
    find_packages,
    setup,
)

FILE_NAME = "VERSION"


EXTRAS = [
    "db",
    "amqp",
    "redis",
]


def get_version():
    with open(FILE_NAME) as file:
        return file.read()


def get_base_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


def get_long_description():
    with open("README.md", encoding="utf-8") as file:
        return file.read()


def get_extras_require():
    all_requires = []
    extras_require = {}

    for extra in EXTRAS:
        with open(f"requirements.{extra}.txt") as file:
            requirements = file.readlines()
            extras_require[extra] = requirements
            all_requires.extend(requirements)

    extras_require["all"] = all_requires

    return extras_require


setup(
    name="popug_sdk",
    version=get_version(),
    package_data={"popug_sdk": ["py.typed"]},
    description="Package for uber popug training project",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Drozdetskiy/popug_jira",
    author="Mikhail Drozdetskiy",
    author_email="m.drozdetskiy.dev@gmail.com",
    packages=find_packages(),
    install_requires=get_base_requirements(),
    extras_require=get_extras_require(),
    include_package_data=True,
    zip_safe=False,
)
