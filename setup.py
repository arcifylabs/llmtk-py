from setuptools import find_packages, setup

# Read version from llmtk/__init__.py
with open("llmtk/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="llmtk",
    version=version,
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "types-setuptools>=75.0.0",
        ],
    },
    python_requires=">=3.9",
    author="Ritik Sahni",
    author_email="ritik@arcifylabs.com",
    description="Type-safe function registration and validation for LLM function calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arcifylabs/llmtk",
    project_urls={
        "Bug Tracker": "https://github.com/arcifylabs/llmtk/issues",
        "Documentation": "https://github.com/arcifylabs/llmtk#readme",
        "Source Code": "https://github.com/arcifylabs/llmtk",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Typing :: Typed",
    ],
    keywords="llm, openai, function-calling, type-safety, validation, pydantic",
)
