from setuptools import setup, find_packages

setup(
    name='chandralc',
    version='0.0.2-alpha',
    packages=find_packages(),
    url='https://github.com/sammarth-k/chandralc',
    license='MIT',
    author='Sammarth Kumar',
    author_email='sam.kumar@yale.edu',
    description='A Python package for CXO lightcurve analysis',
    long_description_content_type = "text/markdown",
    long_description = open('README.md').read(),
    install_requires=['astropy', 'scipy', 'numpy', 'matplotlib', 'requests']
)