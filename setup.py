from setuptools import setup, find_packages

def read_readme() -> str:
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name="MoodApp",
    version="1.0",
    author="Jin-Mach",
    author_email="Ji82Ma@seznam.cz",
    description="A simple application that tracks your current mood.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jin-Mach/MoodApp",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.7.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "mood_app=mood_app:create_app",
            ],
        },
    keywords="mood_app, pyqt6",
)