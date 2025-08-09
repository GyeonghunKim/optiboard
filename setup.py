from pathlib import Path
from setuptools import setup, find_packages

README = Path(__file__).parent / "README.md"
long_description = README.read_text(encoding="utf-8") if README.exists() else ""

setup(
    name="optiboard",
    version="0.1.0",
    description="Lay out and visualize optics breadboards with beam paths",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourname/optiboard",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(exclude=["examples", "tests*"]),
    include_package_data=True,
    install_requires=[
        "numpy>=1.23",
        "matplotlib>=3.6",
        "shapely>=2.0",
    ],
    entry_points={
        "console_scripts": [
            "optiboard=optiboard.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords=["optics", "breadboard", "optomechanics", "visualization"],
)
