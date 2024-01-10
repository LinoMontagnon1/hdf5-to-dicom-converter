import os
import h5py
import pydicom
from pydicom.dataset import Dataset
from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory(title="Selecione a Pasta Contendo os Arquivos HDF5")
dicom_output_folder_name = "DICOM_Output"

base_folder = os.path.dirname(folder_path)
dicom_output_folder = os.path.join(base_folder, dicom_output_folder_name)

if not os.path.exists(dicom_output_folder):
    os.makedirs(dicom_output_folder)

if folder_path:
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".hdf5"):
            hdf5_path = os.path.join(folder_path, file_name)

            try:
                with h5py.File(hdf5_path, 'r') as hdf:
                    if 'entry/data/data' in hdf:
                        data = hdf['entry/data/data'][()]
                    else:
                        print(f"Dataset 'entry/data/data' não encontrado em: {file_name}")
                        continue
                    
                    # Verifica se a imagem é 3D
                    if data.ndim == 3:
                        for i, image_2d in enumerate(data):
                            # Cria um novo dataset DICOM para cada fatia
                            ds = Dataset()

                            ds.is_little_endian = True
                            ds.is_implicit_VR = False

                            ds.PatientID = "123456"
                            ds.PatientName = "lino3"

                            ds.PixelData = image_2d.tobytes()
                            ds.Rows, ds.Columns = image_2d.shape

                            ds.SamplesPerPixel = 1
                            ds.PhotometricInterpretation = "MONOCHROME2"
                            ds.BitsAllocated = 32  
                            ds.BitsStored = 32
                            ds.HighBit = 31
                            ds.PixelRepresentation = 0  

                            dicom_slice_file_name = f"{os.path.splitext(file_name)[0]}_slice_{i}.dcm"
                            dicom_slice_file_path = os.path.join(dicom_output_folder, dicom_slice_file_name)

                            ds.save_as(dicom_slice_file_path)

                            print(f"Arquivo DICOM criado para fatia {i}: {dicom_slice_file_path}")
                    else:
                        print(f"Formato inesperado dos dados em: {file_name}")
            except Exception as e:
                print(f"Erro ao processar o arquivo {file_name}: {e}")

else:
    print("Seleção de pasta cancelada.")
