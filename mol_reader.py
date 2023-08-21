import ase.io
from config import atom_colors, covalent_radii
import numpy as np

class MoleculeReader:

    def __init__(self, args):
        path = args.file

        self.molecules = ase.io.read(path, index = ":")

    def get_N(self):
        return len(self.molecules)
    
    def get_spheres(self, index = 0):
        atoms = self.molecules[index]
        z = atoms.get_atomic_numbers()
        
        radii = covalent_radii[z]
        colors = [f'{c[0]};{c[1]};{c[2]}' for c in atom_colors[z]]
        r = atoms.get_positions()
        r -= np.mean(r, axis = 0)

        return r, radii, colors