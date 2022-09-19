from setuptools import setup


setup(
    name='cm',
    version='0.9.0',
    author='Frank Black',
    author_email='frankblack78@posteo.de',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points="""
        [console_scripts]
        cm=main:cli
    """,
)
