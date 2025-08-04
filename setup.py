from setuptools import setup, find_packages

setup(
    name="netwebscan",
    version="1.0.0",
    author="Krishnamoorthy G",
    description="Advanced CLI Network & Subdomain Scanner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/netwebscan",
    packages=find_packages(),
    install_requires=["colorama>=0.4.6"],
    entry_points={
        "console_scripts": [
            "netwebscan=netwebscan.netwebscan:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
