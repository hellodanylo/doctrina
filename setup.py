import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doctrina",
    version="0.0.1",
    author="Danylo Vashchilenko",
    author_email="dan.vashchilenko@gmail.com",
    description="A library for ML experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellodanylo/doctrina",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)