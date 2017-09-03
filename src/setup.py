from setuptools import setup, find_packages

setup(name='python-wink',
      version='1.5.2',
      description='Access Wink devices via the Wink API',
      url='http://github.com/python-wink/python-wink',
      author='Brad Johnson, William Scanlon',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      zip_safe=True)
