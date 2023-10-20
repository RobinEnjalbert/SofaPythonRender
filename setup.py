from setuptools import setup

PROJECT = 'SofaRender'
with open('README.md') as f:
    long_description = f.read()

setup(name=PROJECT,
      version='23.06',
      description='',
      long_description=long_description,
      author='Robin ENJALBERT',
      author_email='robin.enjalbert@inria.fr',
      url='https://github.com/RobinEnjalbert/SofaPythonRender',
      packages=[PROJECT],
      package_dir={PROJECT: 'src'},
      install_requires=['numpy', 'vedo'])
