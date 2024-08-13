from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyyaml", 
        "python-dotenv"
    ],
    include_package_data=True,
    description="A package for configuration management with environment variables and YAML",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",  # Replace with your GitHub repo or project page
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
