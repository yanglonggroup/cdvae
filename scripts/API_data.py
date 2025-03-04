from mp_api.client import MPRester
import pandas as pd
import numpy as np
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import matplotlib.pyplot as plt
from collections import Counter

# Test connection to Materials Project API
with MPRester(api_key="yRHDRzRRLLAdACIX7ybv1LQeTOIpwDpk") as mpr:
    data1 = mpr.materials.search(material_ids=["mp-4458"])

API_KEY = "yRHDRzRRLLAdACIX7ybv1LQeTOIpwDpk"

def fetch_mp_data(chemsys, num_elements):
    """Searches for designated materials and collects their structural and property data from Materials Project. 
    
    Args:
        chemsys (list): List of chemical systems to search for (e.g., ["Ca-Ti-O", "Ba-Ti-O", "Ca-Fe-O"])
        num_elements (list): List of integers specifying the number of elements in each chemical system (e.g., [3, 3, 3])
    
    Returns:
        dict: A dictionary containing the following material properties:
            - ID: Material IDs
            - Structure: CIF format structures
            - Band Gap: Band gap values in eV
            - Energy Above Hull: Energy above hull values
            - Formation Energy: Formation energy per atom
            - weighted_surface_energy: Weighted surface energy values
            - types_of_magnetic_species: Types of magnetic species present # deleted because of the encoding
            - surface_anisotropy: Surface anisotropy values
            - shape_factor: Shape factor values
    """
    if len(chemsys) != len(num_elements):
        raise ValueError("chemsys_list and num_elements_list must have the same length")
    
    fields=[
                "material_id",
                "structure",
                "formula_pretty",
                "formula_anonymous",
                "band_gap",
                "energy_above_hull",
                'weighted_surface_energy',
                "formation_energy_per_atom",
                "theoretical",
                'types_of_magnetic_species',
                'surface_anisotropy',
                'shape_factor',
    ]
    
    docs = []
    
    with MPRester(API_KEY) as mpr:
        for chemsys, num_elements in zip(chemsys, num_elements):
            docs_temp = mpr.materials.summary.search(
                chemsys=chemsys,
                num_elements=num_elements,
                fields=fields
            )
            docs.extend(docs_temp)
    print(f"Retrieved {len(docs)} potential perovskite structures")
    
    # Extract individual properties from the documents
    substance_id = [substance.material_id for substance in docs]
    substance_structure = [substance.structure.to(fmt='cif') for substance in docs]  
    substance_bandgap = [substance.band_gap for substance in docs]  
    substance_energyabovehull = [substance.energy_above_hull for substance in docs]  
    substance_formenergy = [substance.formation_energy_per_atom for substance in docs]  
    substance_weighted_surface_energy = [substance.weighted_surface_energy for substance in docs]  
    # substance_types_of_magnetic_species = [substance.types_of_magnetic_species for substance in docs]  
    substance_surface_anisotropy = [substance.surface_anisotropy for substance in docs]  
    substance_shape_factor = [substance.shape_factor for substance in docs] 
    
    # Organize data into dictionary
    data = {
        "ID": [s for s in substance_id],
        "Structure": [s for s in substance_structure],  
        "Band Gap": [s for s in substance_bandgap],
        "Energy Above Hull": [s for s in substance_energyabovehull],
        "Formation Energy": [s for s in substance_formenergy],
        "weighted_surface_energy": [s for s in substance_weighted_surface_energy],
        # "types_of_magnetic_species": [s for s in substance_types_of_magnetic_species],
        "surface_anisotropy": [s for s in substance_surface_anisotropy],
        "shape_factor": [s for s in substance_shape_factor],
    }
    data["ID"] = [int(id.replace("mp-", "")) for id in data["ID"]]
    
    return data

def WriteExcel(data, path):
    """Writes material data to an Excel file.
    
    Args:
        data (dict): Dictionary containing material properties to be written to Excel.
    """
    df = pd.DataFrame(data)
    df.to_csv(path, index=False, encoding='utf-8')
        
perovskites = fetch_mp_data(["Ca-Ti-O", "Ba-Ti-O", "Ca-Fe-O"], [3, 3, 3])
WriteExcel(perovskites, "MatDiffusion/MatDiffusion/perovskite_4.xlsx")