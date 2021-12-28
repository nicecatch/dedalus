from distutils.core import setup

setup(
    name='MazeGen',
    version='0.1dev',
    author='Nicecatch',
    url='https://github.com/nicecatch/mazegen/',
    description='Helper for creating mazes with support to solve them',
    packages=['mazegen',],
    install_requires=[
        "numpy >= 1.11.1"
    ]

)