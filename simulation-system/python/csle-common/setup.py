from setuptools import setup

setup(name='csle_common',
      version='0.0.1',
      install_requires=['gym>=0.26.2', 'pyglet>=2.0.0', 'numpy>=1.23.5', 'torch>=1.13.0', 'docker>=6.0.1',
                        'paramiko>=2.12.0', 'stable_baselines3>=1.6.2', 'scp>=0.14.4',
                        'random_username>=1.0.2',
                        'psycopg>=3.1.4', 'click>=8.1.3', 'flask>=2.2.2', 'waitress>=2.1.2', 'csle_collector=0.0.1',
                        'psutil==5.9.4', 'csle-ryu>=0.0.19'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='CSLE is a platform for evaluating and developing reinforcement learning agents for '
                  'control problems in cyber security; csle-common contains the common functionality of csle modules',
      license='Creative Commons Attribution-ShareAlike 4.0 International',
      keywords='Reinforcement-Learning Cyber-Security Markov-Games Markov-Decision-Processes',
      url='https://github.com/Limmen/csle',
      download_url='https://github.com/Limmen/csle/archive/0.0.1.tar.gz',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Programming Language :: Python :: 3.8'
      ]
      )
