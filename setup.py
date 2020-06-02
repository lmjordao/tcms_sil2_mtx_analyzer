from setuptools import setup

setup(name='mtx_analyzer',
      version='0.1.0',
      packages=[],
      entry_points={
          'console_scripts': [
              'mtx_analyzer = __main__:main'
          ]
      }, install_requires=['lxml', 'xlsxwriter']
      )
