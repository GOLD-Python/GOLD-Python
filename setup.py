from distutils.core import setup
setup(
  name = 'gold_python',
  packages = ['gold_python'],
  version = '0.1',
  license='BSD 3-Clause',
  description = 'Library for the developement of finite automata',
  author = 'Nicolas Saavedra Gonzalez',
  author_email = 'personal@nicolassaavedra.com',
  url = 'https://github.com/GOLD-Python/GOLD-Python',
  download_url = 'https://github.com/GOLD-Python/GOLD-Python/archive/refs/tags/v01-BETA.zip',
  keywords = ['automata', 'gold', 'transducer', 'pushdown', 'deterministic'],
  install_requires=[
          'networkx',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
