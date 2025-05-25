#!/usr/bin/env python
# setup.py

import setuptools

setuptools.setup(
    name="todo-task-node-tree",                   
    version="0.1.1",                    
    description="📌 基于 Typer 与 Rich 的命令行 Todo 工具",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="RinKokokawa",
    author_email="rin@rinco.cc", 
    url="https://github.com/RinKokawa/todo-cli",
    license="MIT",
    python_requires=">=3.13",
    packages=setuptools.find_packages(),
    py_modules=["app"],
    
    install_requires=[
        "typer>=0.7.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "todo = app:app",  ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
