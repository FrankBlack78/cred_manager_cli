from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements


setup(
    name='cm',
    version='0.1.0',
    author='Frank Black',
    author_email='frankblack78@posteo.de',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['main'],
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        cm=main:cli
    """,
)
