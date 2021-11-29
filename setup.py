from setuptools import setup, find_packages

setup(
    name='chandralc',
    version='0.0.1-alpha',
    packages=find_packages(),
    url='https://github.com/sammarth-k/chandralc',
    license='MIT',
    author='Sammarth Kumar',
    author_email='kumarsammarth@gmail.com',
    description='A Python package for CXO lightcurve analysis',
    long_description_content_type = "text/markdown",
    long_description = open('README.md').read(),
    install_requires=['astropy', 'scipy', 'numpy', 'matplotlib', 'requests']
)