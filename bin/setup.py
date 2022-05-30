from setuptools import setup

setup(
    name='csle-cli',
    version='0.0.1',
    py_modules=['csle-cli'],
    install_requires=[
        'Click',
        'csle-common', 'csle-collector', 'csle-attacker', 'csle-defender',
        'csle-system-identification', 'gym-csle-stopping-game', 'stable-baselines3'
    ],
    entry_points='''
        [console_scripts]
        csle=csle-cli.csle:commands
    ''',
)