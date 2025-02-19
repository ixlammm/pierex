from setuptools import setup

setup(
    name="pierex",
    version="0.1.0",
    packages=["pierex"],
    entry_points={
        "console_scripts": [
            "pierex=pierex.pierex:main",
        ],
    },
    author="Islam Tazerout",
    author_email="islamtazerout3@gmail.com",
    description="A Python tool for watching files and directories",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ixlammm/pierex",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)