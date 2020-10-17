import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lki", # Replace with your own username
    version="0.0.1",
    author="Aleksas Pielikis",
    author_email="ant.kampo@gmail.com",
    description="LKI datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aleksas/lki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)