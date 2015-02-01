from setuptools import setup

setup(name='python-guidestar',
      version='0.1.1',
      description='Python client library for Guidestar API',
      url='http://github.com/rmaceissoft/python-guidestar',
      author='Reiner Marquez',
      author_email='rmaceissoft@gmail.com',
      license='MIT',
      packages=['guidestar'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
