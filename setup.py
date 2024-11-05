from setuptools import setup, find_packages

setup(
    name="llama-chat-sdk",
    version="1.0.0",
    description="A Python SDK for the Llama Chat API",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Aryan",
    author_email="agarwalaryan139@gmail.com",
    url="https://github.com/thearyanag/llama-chat-sdk",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)