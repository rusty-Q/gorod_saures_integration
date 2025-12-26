from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uk-saures-integration",
    version="1.0.0",
    author="rusty-Q",
    author_email="rustam2701@yandex.ru",
    description="Интеграция данных счетчиков из UK_GOROD и Saures API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rusty-Q/hass-saures",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0-only",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "PyYAML>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "uk-saures-integrate=uk_saures_integration.cli:main",
        ],
    },
)
