from setuptools import setup, find_packages

setup(
    name="botmaster",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.11.0",
        "langchain-community>=0.0.10",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "pydantic>=2.5.2",
        "litellm>=1.15.0",
        "openai>=1.3.0"
    ],
) 