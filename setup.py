from setuptools import setup, find_packages
from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


with open('requirements.txt', "r") as f:
    install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version.txt") as f:
    version = f.read()

setup(
    name='flaretool',  # パッケージ名（pip listで表示される）
    version=version,  # バージョン
    description="this is flarebrow package",  # 説明
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://main.flarebrow.com",
    author='flarebrow',  # 作者名
    license='MIT',  # ライセンス
    keywords='flaretool',
    packages=find_packages("repos"),
    package_dir={"": "repos"},
    py_modules=[splitext(basename(path))[0] for path in glob('repos/**/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'flaretool=flaretool.command:main',
        ],
    },
    project_urls={
        "Documentation": "https://flarebrow.github.io/flaretool/",
        "Source": "https://github.com/flarebrow/flaretool",
    },
)
