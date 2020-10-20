import setuptools
import re, ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('lki/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="lki",
    version=version,
    author="Aleksas Pielikis",
    author_email="ant.kampo@gmail.com",
    description="LKI datasets",
    install_requires=requirements,
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