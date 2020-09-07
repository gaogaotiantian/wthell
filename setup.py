import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("./src/wthell/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

setuptools.setup(
    name="wthell",
    version=version,
    author="Tian Gao",
    author_email="gaogaotiantian@hotmail.com",
    description="A debugging tool that can help you what happened when you code quits unexpectedly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaogaotiantian/wthell",
    packages=setuptools.find_packages("src"),
    package_dir={"":"src"},
    install_requires=[
        "rich"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    entry_points={
        "console_scripts": {
            "wthell = wthell:main"
        }
    }
)
