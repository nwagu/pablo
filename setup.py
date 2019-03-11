setup(
    name="Pablo",
    version="0.1",
    description="An collaborative text editor for writers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nwagu/pablo",
    author="Chukwuemeka Nwagu",
    author_email="developer.nwagu@gmail.com",
    license="LGPL",
    classifiers=[
        "License :: OSI Approved :: LGPL License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["pablo"],
    include_package_data=True,
    install_requires=[
        "pyside2", "Pillow", "scipy", "numpy", "requests"
    ],
    entry_points={"console_scripts": ["pablo=__main__:main"]},
)