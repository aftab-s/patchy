"""
Setup script for the GitHub Discord Webhook Bot.

This script provides a convenient way to install the bot and its dependencies.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="patchy-github-discord-webhook-bot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Patchy - A Discord bot that receives GitHub webhook events and sends formatted notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/github-discord-webhook-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Version Control",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "patchy-github-discord-bot=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
