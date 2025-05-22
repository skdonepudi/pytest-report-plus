from setuptools import setup, find_packages

setup(
    name="pytest_reporter",
    version="0.1.0",
    packages=find_packages(),
    description="Lightweight JSON test reporter for Pytest",
    author="Your Name",
    license="MIT",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "pytest_json_reporter = pytest_json_reporter.generate_html_report:main"
        ]
    }
)
