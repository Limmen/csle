from setuptools import setup, find_packages

setup(name='csle_collector',
      version='0.0.38',
      install_requires=['grpcio-tools', 'scipy', 'confluent-kafka', 'docker'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='scripts for data collection in CSLE',
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