import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# automatically captured required modules for install_requires in requirements.txt
with open("requirements.txt", encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if
                    (not x.startswith('#')) and (not x.startswith('-'))]

setuptools.setup(
    name="redditsearcher-arcanee",  # Replace with your own username
    version="2.0.0b2",
    author="Leonardo Coppi",
    author_email="leoman.coppi@gmail.com",
    description="A program for generating csv files to see the most mentioned \
                and highest scoring US tickers in inputted reddit subreddits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheArcanePowers/Stock-Scraper",
    project_urls={
        "Bug Tracker": "https://github.com/TheArcanePowers/Stock-Scraper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: Free To Use But Restricted",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "Natural Language :: English"
    ],
    install_requires=install_requires,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
