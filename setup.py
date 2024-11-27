from setuptools import setup, find_packages

setup(
    name="django-protego",
    version="0.0.1",
    description="A lightweight circuit breaker library for Django",
    author="Fauzan",
    author_email="muqhul@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
