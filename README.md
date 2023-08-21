# Timol

Timol (Terminal Interface MOLecular visualiser) is a way to display the 3D structure of a molecule natively inside a terminal. The camera can be moved with the mouse and zoomed in/out by scrolling. 

## Installation

The software is not yet packaged and needs to have its dependencies installed manually:

`pip install scipy ase pytermgui` 

## Running Timol

The software is not yet packaged so running the visualiser is done manually:

`python main.py <name_of_mol_file>` 

Currently, `.npz` is supported as well as all file types supported by ase (`.xyz`, `.db`, ...)

## Todo list

- Package
- Allow changing indices (currently just index 0 of file)
- Allow moving camera centre
- Fix occasional crashing when the camera moves excessively
- Atom edges somewhow (esp. for bigger molecules or crystals)
