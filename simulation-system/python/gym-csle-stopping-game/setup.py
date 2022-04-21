from setuptools import setup

setup(name='gym_csle_stopping_game',
      version='0.0.1',
      install_requires=['gym', 'pyglet', 'numpy', 'torch', 'docker', 'paramiko', 'stable_baselines3', 'scp',
                        'random_username', 'Sphinx', 'sphinxcontrib-napoleon',
                        'sphinx-rtd-theme', 'csle-common', 'pyperclip', 'psycopg', 'click', 'csle-attacker',
                        'csle-defender', 'csle-collector'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='CSLE is a platform for evaluating and developing reinforcement learning agents for '
                  'control problems in cyber security; gym-csle-stopping-game implements an optimal '
                  'stopping game in CSLE',
      license='Creative Commons Attribution-ShareAlike 4.0 International',
      keywords='Reinforcement-Learning Cyber-Security',
      url='https://github.com/Limmen/csle',
      download_url='https://github.com/Limmen/csle/archive/0.0.1.tar.gz',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Programming Language :: Python :: 3.8'
      ]
)