import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harmalysis", # Replace with your own username
    version="0.1.0",
    author="Nestor Napoles Lopez",
    author_email="napulen@gmail.com",
    description="A language for harmonic analysis and roman numerals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/napulen/harmalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
