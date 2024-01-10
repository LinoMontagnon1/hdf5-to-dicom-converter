import h5py

def print_structure(hdf_object, indent=0):
    """Função recursiva para imprimir a estrutura de um objeto HDF5."""
    for key in hdf_object.keys():
        item = hdf_object[key]
        print('  ' * indent + f"- {key}: {type(item)}")
        if isinstance(item, h5py.Dataset):
            print('  ' * (indent+1) + f"Shape: {item.shape}, Dtype: {item.dtype}")
        elif isinstance(item, h5py.Group):
            print_structure(item, indent+1)

#path
file_path = "C:\\Users\\Lino\\Downloads\\2023_11_22_cilindro_assimetrico\\2023_11_22_cilindro_assimetrico\\flaten\\flaten_cilindo_assime_HGM_70cm_50kVp_1200microAs_0000.hdf5"

with h5py.File(file_path, 'r') as hdf:
    print_structure(hdf)
