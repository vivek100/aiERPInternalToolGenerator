from setuptools import setup, find_packages

setup(
    name="ai-code-generator-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "rich",
        "langchain",
        "langchain-anthropic",
        "langchain-community",
        "openai",
        "anthropic",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "codegen=src.cli:main",
        ],
    },
) 