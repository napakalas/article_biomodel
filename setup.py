import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='article_biomodel',
    version='0.0.1',
    author="Yuda Munarko",
    author_email="yuda.munarko@gmail.com",
    description="A tool to classify an article to biomodel or not",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/napakalas/article_biomodel",
    packages=setuptools.find_packages(),
    install_requires=[
        'gdown',
        'transformers',
        'biopython',
        'tqdm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    # package_data={'': ['*resources/*','sedmlImages/*']},
)
