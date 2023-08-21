import ase.io
from config import atom_colors, covalent_radii
import numpy as np

class MoleculeReader:
    ase = False
    npz = False
    def __init__(self, args):
        path = args.file

        if path.endswith('.npz'):
            data = np.load(path)
            self.molecules = [data['R'][0]]
            self.z = data['z']
            self.npz = True

        else:
            # self.molecules = ase.io.read(path, index = ":")
            self.molecules = [ase.io.read(path, index = 0)]
            self.ase = True

    def get_N(self):
        return len(self.molecules)
    
    def get_atomic_numbers(self, index):
        if self.ase:
            atoms = self.molecules[index]
            return  atoms.get_atomic_numbers()
        
        if self.npz:
            return self.z
        
    def get_positions(self, index):
        if self.ase:
            atoms = self.molecules[index]
            return atoms.get_positions()
        
        if self.npz:
            return self.molecules[index]      

    def get_spheres(self, index = 0):
        z = self.get_atomic_numbers(index)
        
        radii = covalent_radii[z]
        colors = [f'{c[0]};{c[1]};{c[2]}' for c in atom_colors[z]]
        r = self.get_positions(index)
        r -= np.mean(r, axis = 0)

        return r, radii, colors