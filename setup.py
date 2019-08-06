from pathlib import Path

from setuptools import setup

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="malloc",
    version="0.2.0",
    url="https://github.com/thg-consulting/malloc",
    author="thg",
    py_modules=["malloc"],
    description="PyMem_ family interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
