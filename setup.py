from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smretriever",
    version="0.1.0",
    author="Fundación Santo Domingo",
    author_email="info@funsd.org",
    description="A library for retrieving SurveyMonkey data through R integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fundacionsantodomingo/smretriever",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "rpy2>=3.5.0",
    ],
) 