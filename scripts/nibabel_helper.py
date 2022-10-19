import os
import nibabel as nb
import numpy as np

# some helper functions for tonotopy data parsing


def get_spmf_files_as_list(path):
    "returns a list of all spmf files in a directory"
    spmf_files = []
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if x.startswith("spmF_"):
                spmf_files.append(os.path.join(dirpath, x))
    return spmf_files


def get_save_affine(nifti_file, path):
    "saves the affine as np array on disk from a nifti file"
    nifti = nb.load(nifti_file)
    affine = nifti.affine
    np.save(path, affine)


def average_np_arrays(np_arrays):
    # returns a averaged single array from multiple np arrays
    init_array = np.zeros(np_arrays[0].shape)
    for arr in np_arrays:
        init_array += arr

    averaged_np_array = init_array / len(np_arrays)
    return averaged_np_array


def save_nifti_image(fdata, affine, path):
    # saves a new nifti image to a path
    new_image = nb.Nifti1Image(fdata, affine)
    nb.save(new_image, path)


def save_average_spmf_file(spmf_files, affine, path):
    nifti_fdata_list = []

    for spmf in spmf_files:
        nifti_data = nb.load(spmf)
        nifti_fdata = nifti_data.get_fdata()
        nifti_fdata_list.append(nifti_fdata)

    averaged_spmf = average_np_arrays(nifti_fdata_list)
    save_nifti_image(averaged_spmf, affine, path)


