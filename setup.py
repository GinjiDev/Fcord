import setuptools
import os

def read_file(path):
    with open(path, "r") as fp:
        return fp.read()

def install_requires():
    requirements = read_file(os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements.txt")).split("\n")
    requirements = list(filter(lambda s: not not s, map(lambda s: s.strip(), requirements)))

    return requirements

long_description = read_file("README.md")

setuptools.setup(
    name="Fcord_api",
    version="0.0.1",
    author="ShadDigo,Maxsspeaker",
    description="Автоматическое обновление статистики вашего бота на платформе Fcord.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mivian.ru/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires(),
    python_requires='>=3.9',
)
