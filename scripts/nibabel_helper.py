import os
import nibabel as nb
import numpy as np
import glob
import os

# datapath = "/home/milan/Documents/school/projects/tonotopy_pipeline/Tonotopy/"

# SAMPLES = [os.path.basename(x) for x in glob.glob("/home/milan/Documents/school/projects/tonotopy_pipeline/Tonotopy/con3810/Functional/lswzTask/")]
# print(SAMPLES)

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



def filter_significant_voxels(beta, averaged_spmf, min_v, save_path):
    """
    Filters significant voxels from a beta file using an averaged spmf map and min_v value as treshold
    """
    # print("FILTERING BETAS")
    load_beta = nb.load(beta)
    beta_fdata = load_beta.get_fdata()
    shape = beta_fdata.shape
    affine = load_beta.affine
    spmf_fdata = nb.load(averaged_spmf).get_fdata()
    init_array = np.zeros(shape)
    init_array[spmf_fdata > min_v] = beta_fdata[spmf_fdata > min_v]
    save_nifti_image(init_array, affine, save_path)