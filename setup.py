from setuptools import setup, find_packages

setup(
    name='ChemMLP',
    version='0.1',
    author='AtomixAI',
    author_email='sadollah.ebrahimi@usherbrooke.ca',
    packages=find_packages(),
    install_requires=[
        #'python >= 3.6'
        'numpy',
        'pandas',
        'matplotlib',
        'rdkit',
        'scikit-learn',
        'keras',
        'PyQt5',
        'PySide2',
        'tensorflow',
        
        
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'mycommand=P.main:main',
        ],
    },
)
