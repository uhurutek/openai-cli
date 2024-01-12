from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='openai-cli',
    version='0.1.0',
    packages=[''],
    url='https://github.com/uhurutek/openai-cli',
    license='MIT',
    author='imtiaz-rahi',
    author_email='imtiaz.rahi@gmail.com',
    description='Command line (CLI) application of OpenAI python client library',
    long_description=long_description,
    project_urls={
        "Bug Reports": "https://github.com/uhurutek/openai-cli/issues",
        "Source": "https://github.com/uhurutek/openai-cli",
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by "pip install". See instead "python_requires" below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    package_dir={""},
    install_requires=["python-dotenv", "click", "openai",],
)
