from setuptools import setup, find_packages

setup(
    name='csle_cli',
    version='0.0.1',
    py_modules=['csle_cli'],
    author='Kim Hammar',
    description='CLI tool for CSLE',
    author_email='hammar.kim@gmail.com',
    license='Creative Commons Attribution-ShareAlike 4.0 International',
    keywords='Reinforcement-Learning Cyber-Security Markov-Games Markov-Decision-Processes',
    url='https://github.com/Limmen/csle',
    download_url='https://github.com/Limmen/csle/archive/0.0.1.tar.gz',
    packages=find_packages(),
    install_requires=[
        'Click>=8.0.0',
        'csle-common', 'csle-collector', 'csle-attacker', 'csle-defender',
        'csle-system-identification', 'gym-csle-stopping-game', 'stable-baselines3'
    ],
    entry_points='''
        [console_scripts]
        csle=csle_cli.cli:commands
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3.8'
    ]
)