from setuptools import setup, find_packages

setup(
        name='mqlTradeSim',
        version='0.1.0.1',
        description='MQL Trade Simulator',
        long_description=open("README.md").read(),
        author='Yongseok Jang',
        author_email='turboce@gmail.com',
        url='https://github.com/TurboCE/mqlTradeSim/',
        license='MIT',
        python_requires='>=3',
        packages=find_packages(),
        classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
        ],
    )
