# https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
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
    long_description_content_type="text/markdown",
    keywords="openai, cli, command-line",
    project_urls={
        "Bug Reports": "https://github.com/uhurutek/openai-cli/issues",
        "Source": "https://github.com/uhurutek/openai-cli",
    },
    classifiers=[
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
    install_requires=["python-dotenv", "click", "openai", ],
    entry_points='''
    [console_scripts]
    openai-asst=openai_asst:main
    openai-cli=openai_cli:main
    '''
)
