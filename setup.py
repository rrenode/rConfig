from setuptools import setup, find_packages
import pathlib

# Read the requirements.txt file
HERE = pathlib.Path(__file__).parent
with open(HERE / "requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="rConfig",
    version="0.1",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    description="A package for configuration management with environment variables and YAML. Has a definitely creative name.",
    author="Robert J Renode IV",
    url="https://github.com/rrenode/rConfig",  # Replace with your GitHub repo or project page
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
