from setuptools import setup, find_packages

setup(name='csle_agents',
      version='0.0.1',
      install_requires=['csle-common', 'csle-collector', 'csle-attacker', 'csle-defender',
                        'csle-system-identification', 'gym-csle-stopping-game', 'stable-baselines3', 'pulp'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='Reinforcement learning agents for CSLE',
      license='Creative Commons Attribution-ShareAlike 4.0 International',
      keywords='Reinforcement-Learning Cyber-Security Markov-Games Markov-Decision-Processes',
      url='https://github.com/Limmen/csle',
      download_url='https://github.com/Limmen/csle/archive/0.0.1.tar.gz',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Programming Language :: Python :: 3.8'
      ]
      )