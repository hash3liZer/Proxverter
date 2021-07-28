import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proxverter",
    version="0.1",
    author="hash3liZer",
    author_email="admin@shellvoide.com",
    description="Reverse proxy & TLS Interception library for Python. Basically a wrapper around proxy.py and OpenSSL allowing easy integration and certificate generation on command (Under Development)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hash3liZer/Proxverter",
    project_urls={
        "Bug Tracker": "https://github.com/hash3liZer/Proxverter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    packages=['proxverter', 'proxverter.plugins'],
    python_requires=">=3.7",
    install_requires=[
        'pyopenssl',
        'proxy.py'
    ]
)
