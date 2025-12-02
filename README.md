README
======

Algorithm & Data Structure Visualizer is a small desktop program written in
Python. It animates classic algorithms step by step, mainly focusing on
sorting for now. The goal is to make it easier to *see* what the code is
doing: comparisons, swaps and the evolving state of the array.

Use this program if you want a visual aid for teaching, learning or revising
basic algorithm design and complexity.

You can change:

  * which sorting algorithm is used
  * the size of the dataset
  * how fast the animation runs
  * whether it runs automatically or one step at a time

BUILD AND RUN
=============

You need Python 3 and the PySide6 library installed.

To install the dependency:

  python3 -m pip install PySide6

To run the program from the project root:

  python3 -m algo_visualizer.main

If everything works, a window will appear with controls at the top and a bar
chart in the center that shows the array as it is being sorted.

DIRECTORY STRUCTURE
===================

The interesting files live in the algo_visualizer package:

  algo_visualizer/
      main.py            - entry point that starts the GUI
      algorithms/        - algorithm implementations
          __init__.py
          sorting.py     - bubble, insertion and selection sort generators
      ui/                - user interface components
          __init__.py
          main_window.py - main window, controls, timer logic
          visualizer_canvas.py - custom drawing surface for the bars

The sorting algorithms are implemented as Python generators that yield each
intermediate state: (array, index_a, index_b). The UI advances through these
states using a timer or a single-step button.

CONTACT
=======

If you have problems, questions, ideas or suggestions, please open an issue
or discussion on the GitHub project page:

  https://github.com/arengharibian/Algorithm-Data-Structure-Visualizer/issues

WEBSITE
=======

Visit the GitHub repository for the latest code, notes and updates:

  https://github.com/arengharibian/Algorithm-Data-Structure-Visualizer

GIT
===

To clone the very latest source from GitHub, do this:

  git clone https://github.com/arengharibian/Algorithm-Data-Structure-Visualizer.git

You will get a directory created with the source code for the visualizer.

SECURITY PROBLEMS
=================

This project is a local teaching tool and does not expose any network-facing
services. If you still believe you have found a security issue, please open
a private issue or contact the maintainer rather than posting details in
public first.

NOTICE
======

This project is provided for educational purposes. You are free to read the
code, learn from it and adapt it for your own experiments. If you redistribute
modified versions, please include a note so people know it is not the original
repository.

See the LICENSE file for full distribution terms.
