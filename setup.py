from setuptools import setup, find_packages

setup(
    name="flagsmith-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "inquirer>=3.1.3",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "flagsmith=flagsmith_cli.cli:main",
        ],
    },
    python_requires=">=3.8",
)