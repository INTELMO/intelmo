from setuptools import find_packages
from setuptools import setup

with open('README.md', "r") as f:
    long_description = f.read()

print(find_packages(
    exclude=["examples", "tests", "docs"],
))


setup(
    name='intelmo',
    version='1.0.3',
    description='Interface Toolkit for Extensive Language Models',
    long_description=long_description,
    author="Chunxu Yang",
    author_email="chunxuyang@ucla.edu",
    # include_package_data=True,
    packages=find_packages(
        exclude=["examples", "tests", "docs"],
    ),
    include_package_data=True,
    package_data={
        'templates': ["intelmo/templates/*"],
        'static': ["intelmo/static/*"],
    },
    zipSafe=False,
    install_requires=[
        'flask',
        'flask-cors',
        'newspaper3k',
        'nltk',
        'feedparser',
        'pydantic',
    ],
    license='MIT',
    platforms=["all"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
