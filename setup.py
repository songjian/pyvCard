import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vCard",
    version="0.0.1",
    author="sj",
    author_email="songjian@codeorder.cn",
    description="Python操作Android手机联系人的包。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/songjian/vCard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'uiautomator2==2.16.19',
        'vobject==0.9.6.1'
    ],
    python_requires='>=3'
)