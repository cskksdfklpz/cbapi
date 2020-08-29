from setuptools import setup

setup(

    name="cbapi",
    author="Quanzhi(Allen) Bi",
    packages=["cbapi"],
    version="1.0.0",
    description="Full-featured API library to allow downloading and presenting organization and people data from Crunchbase",
    long_description=open('README.md').read(),
    install_requires=['requests','pandas','numpy','psutil']

)