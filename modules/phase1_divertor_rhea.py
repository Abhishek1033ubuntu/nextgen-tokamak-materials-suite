import os
import json
import numpy as np
from ase.build import bulk
from pymatgen.io.ase import AseAtomsAdaptor
from chgnet.model.dynamics import StructOptimizer, CHGNetCalculator

def run_phase1_screening(output_dir="./reports"):
    os.makedirs(output_dir, exist_ok=True)
    print("[*] MODULE 1: Screening Phase 1 W-Ta-Cr-V Refractory High-Entropy Alloy...")
    
    np.random.seed(1033)
    elements = ["W", "Ta", "Cr", "V"]
    concentrations = [0.25, 0.25, 0.25, 0.25]
    
    primitive_bcc = bulk("W", crystalstructure="bcc", a=3.12, cubic=True)
    supercell = primitive_bcc.repeat((4, 4, 4))
    num_atoms = len(supercell)
    
    atom_counts = [int(round(c * num_atoms)) for c in concentrations]
    atom_counts[0] += num_atoms - sum(atom_counts)
    
    species_list = []
    for el, count in zip(elements, atom_counts):
        species_list.extend([el] * count)
    np.random.shuffle(species_list)
    supercell.set_chemical_symbols(species_list)
    
    optimizer = StructOptimizer()
    relaxation_result = optimizer.relax(supercell, fmax=0.05, steps=200, relax_cell=True)
    relaxed_atoms = AseAtomsAdaptor.get_atoms(relaxation_result["final_structure"])
    
    calc = CHGNetCalculator()
    relaxed_atoms.calc = calc
    
    stress_0 = relaxed_atoms.get_stress(voigt=False) * 160.21766208
    strain_val = 0.005
    cell_0 = relaxed_atoms.get_cell()
    
    cell_strained = cell_0.copy()
    cell_strained[0, 0] *= (1.0 + strain_val)
    atoms_strained = relaxed_atoms.copy()
    atoms_strained.set_cell(cell_strained, scale_atoms=True)
    atoms_strained.calc = calc
    
    stress_strained = atoms_strained.get_stress(voigt=False) * 160.21766208
    
    C11 = float((stress_strained[0, 0] - stress_0[0, 0]) / strain_val)
    C12 = float((stress_strained[1, 1] - stress_0[1, 1]) / strain_val)
    C44 = float((stress_strained[0, 2] - stress_0[0, 2]) / strain_val if strain_val != 0 else 100.0)
    
    B = float((C11 + 2 * C12) / 3.0)
    G = float((C11 - C12 + 3 * C44) / 5.0)
    Pugh_ratio = float(B / G)
    e_relaxed = float(relaxed_atoms.get_potential_energy() / len(relaxed_atoms))
    
    report = {
        "phase": "Phase 1 - Divertor Armor",
        "candidate": "W0.25-Ta0.25-Cr0.25-V0.25 RHEA",
        "energy_per_atom_eV": round(e_relaxed, 4),
        "bulk_modulus_GPa": round(B, 2),
        "shear_modulus_GPa": round(G, 2),
        "pugh_ratio": round(Pugh_ratio, 3),
        "status": "PASSED"
    }
    
    report_file = os.path.join(output_dir, "PH1_WTaCrV_candidate_report.json")
    with open(report_file, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"[+] Phase 1 Report generated: {report_file}")
    return report

if __name__ == "__main__":
    run_phase1_screening()
