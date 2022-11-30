import nibabel as nb
import numpy as np



def create_average_map(nii_files):
    # Creates an averaged map from a list of nii files

    nii_list = [nb.load(x) for x in nii_files]
    shape_init = nii_list[0].shape
    summed_array = np.zeros(shape_init)

    for i in nii_list:
        f_data = i.get_fdata()
        summed_array += f_data

    averaged_array = summed_array / len(nii_list)

    return averaged_array








