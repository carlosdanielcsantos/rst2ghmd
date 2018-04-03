from setuptools import setup

setup(name='rst2ghmd',
      version='0.1.0',
      author='Carlos Daniel Santos',
      description='Convert RST to GitHub MD',
      packages=['rst2ghmd'],
      entry_points={
          'console_scripts': ['rst2ghmd=rst2ghmd.cli:main'],
      },
      platforms='any')
