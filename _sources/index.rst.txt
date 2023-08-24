GOLD-Python
===========

The GOLD-Python proyect is a Python package with the objective of providing a
simple and easy to use interface to the GOLD programming language's finite automata
library.

It supports Windows, Linux and Mac OS X, and works with Python 3.10 and 3.11.

The GOLD-Python library, along with this documentation is licensed under the BSD-3 3-Clause License. See the LICENSE file for more information.

.. code:: python

   automaton = createAutomaton()
   accepted = automaton.accepts_input(input("Enter: "))
   if accepted:
      print("Accepted")
   else:
      print("Rejected")

   def createAutomaton():
      Q = product(between(0, 7), between(0, 1))
      E = "01"
      Q0 = (0, 0)
      F = [(0, 0)]

      return DeterministicAutomata(Q, E, Q0, F, delta)

   @deltafunc
   def delta(x, y, next):
      d = int(next)
      if (x, y) == (0, 1):
         return (0, 1)
      elif x==7:
         return (0, 0) if (d-y==0) else (0, 1)
      else:
         return (x+1, (y+d) % 2)

Getting Started
===============

.. toctree::
   :caption: Getting Started
   :hidden:

   installing
   first_steps
   contributing

:doc:`installing`
   Insalling GOLD-Python in your proyect

:doc:`first_steps`
   Creating your first finite automata

:doc:`contributing`
   Contributing to the GOLD-Python project

Documentation
=============

.. toctree::
   :caption: Documentation
   :hidden:

   automata
   sets
   delta

:doc:`automata`
   Documentation of all the automata's available in GOLD-Python

:doc:`sets`
   Documentation of all the set operations given by GOLD-Python

:doc:`delta`
   Documentation of all the delta decorators in GOLD-Python

Reference
=========

.. toctree::
   :caption: Reference
   :hidden:

   changelog
   license

:doc:`changelog`
   Changelog of the GOLD-Python project

:doc:`license`
   License of the GOLD-Python project
