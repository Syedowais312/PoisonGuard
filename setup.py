from setuptools import setup, find_packages


setup(
    name="poisonguard",
    version="0.1.0",

    packages=find_packages(),

    install_requires=[
        "fastapi",
        "requests",
        "uvicorn",
        "sentence-transformers",
        "scikit-learn",
        "joblib"
    ],

    author="Your Team",

    description="Middleware security plugin for RAG poisoning attacks",
)
