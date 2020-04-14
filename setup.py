from setuptools import setup, find_packages

setup(name='mqlTradeSim',
          version='0.3.0.1',
          description='MQL Trade Simulator',
          author='Yongseok Jang',
          author_email='turboce@gmail.com',
          url='https://dekaf.mizzy.kr'​,
          license='MIT',
          py_modules=['mqlTradeSim'],
          python_requires='>=3',
          include_package_data=True,
          package_data={
                 'mqlTradeSim': [
                ]},
         ​packages=['mqlTradeSim'],
         zip_safe=False
    )
