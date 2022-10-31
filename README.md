# GOLD-Python

GOLD-Python is a port of the GOLD programming language's Finite Automata features to Python 3.10 for a better developer experience.

## How to install

```sh
pip install gold-python
```

## Using the library:

```python
def main():
    automaton = createAutomaton()
    print(automaton.acceptsInput(input("Enter: ")))
    automaton.show()


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

if __name__ == "__main__":
    main()
```

## Features:

* Better Syntax Autocompletion
* Support for types
* Docstrings for most functions
* Documentation in HTML (work in progress)

## Progress:

* ~~Deterministic Finite State Automata~~
* ~~Deterministic Transducer (Mealey)~~
* ~~Basic Set Operations (Between, Product)~~
* ~~Non-Deterministic Finite State Automata~~
* Pushdown Automata
* Advanced Set Operations (String ranges, Parts of sets, etc)
* GUI Interface to show Automata
* Full documentation in Sphinx (Progress: 0%)
* Release
