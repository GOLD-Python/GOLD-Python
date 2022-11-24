**********
Installing
**********

Instalation from `PyPI <https://pypi.org/project/gold-python/>`__
===================================================================

1. Make sure you have Python 3.10+ in your PATH (see http://www.python.org/download/).

2. Open a command prompt and type:

.. code:: python

    pip install gold-python

.. Attention:: We do not support Python 3.9 or earlier for the time being. This includes the latest version of Anaconda. Make sure you are using the Python installation from python.org instead of Anaconda before reporting any issues.

Building from source
====================

1. Clone the repository:

.. code:: bash

    git clone https://github.com/GOLD-Python/GOLD-Python

2. Install the dependencies:

.. code:: bash

    pip install -r requirements.txt

3. Install the package:

.. code:: bash

    python setup.py install

.. Danger:: No suppport will be provided for building from source. Please use the pip package instead. If you wish to contribute to the project, please see the contributing guide.

Building the documentation
==========================

1. Clone the repository:

.. code:: bash

    git clone https://github.com/GOLD-Python/GOLD-Python

2. Install sphinx:

.. code:: bash

    pip install sphinx

3. Run the build script:

.. code:: bash

    make html

The documentation will be in the docs/_build/html folder.

.. Note:: If you are using Windows, you may need to install make for Windows. See https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows for more information. To support the documentation, please see the contributing guide.
