from setuptools import setup, find_packages

setup(name='csle_rest_api',
      version='0.0.1',
      install_requires=['flask>=2.2.2', 'waitress>=2.1.2', 'flask-socketio>=5.3.2',
                        'csle-common==0.0.1', "csle-agents==0.0.1",
                        "csle-system-identification==0.0.1", "csle-ryu>=0.0.19", 'bcrypt>=4.0.1',
                        'pyopenssl>=22.1.0',
                        'eventlet>=0.33.2', 'gevent>=22.1.2'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='CSLE REST API',
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
