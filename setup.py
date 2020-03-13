from setuptools import setup

setup(name='mtx_analyzer',
      version='0.1.0',
      packages=['src'],
      entry_points={
          'console_scripts': [
              'mtx_analyzer = src.__main__:main'
          ]
      }, install_requires=['lxml', 'xlsxwriter']
      )
