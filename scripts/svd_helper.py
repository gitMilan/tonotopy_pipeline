# assortment of functions for performing matrices and SVDs
from os import listdir
from os.path import isfile, join
import numpy as np
import nibabel as nb
import pandas as pd
import dask
import dask.array as da
import math
import re



def get_betas_from_subject(subject_path):
    betas = [f for f in listdir(subject_path) if isfile(join(subject_path, f))]


def flatten_np_array(np_arr):
    return np_arr.flatten()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_flattened_fdata(beta):
    fdata = nb.load(beta).get_fdata()
    flatten = fdata.flatten()
    return flatten


def f_data_array_from_beta_list(betas):
    """Makes an f_data_list from the beta list."""
    f_data_list = []
    for beta in betas:
        f_data = nb.load(beta).get_fdata().flatten()
        f_data_list.append(f_data)
    f_data_array = np.array(f_data_list)
    concentated = np.concatenate(f_data_array)

    return concentated


def get_subjects_ordered(beta_files, n_betas):
    """
    This function is needed to extract the subjects in the same order as the SVD matrix is constructed,
    otherwise this information is lost.
    """
    beta_files = list(chunks(sorted(beta_files), n_betas))
    subjects = []

    for subject in beta_files:
        subject = re.search("(con|tin|los)\d+", subject[1])[0]
        subjects.append(subject)

    return subjects


def get_shape(beta_file):
    nifti = nb.load(beta_file)
    shape = nifti.shape
    return shape


def create_fdata_matrix(beta_files, n_betas):
    """Created a 2d matrix from a list of beta files. The input list is ordered and arranged to that
    the columns are the different betas and de rows are subjects"""

    beta_files = list(chunks(sorted(beta_files), n_betas))
    data_struct = []
    for col in range(n_betas):
        column_data = [i[col] for i in beta_files]
        fdata = f_data_array_from_beta_list(column_data)
        data_struct.append(fdata)

    arr1 = np.vstack(data_struct).T

    return arr1


def save_arr(path, arr):
    np.save(path, arr)  # save


def split_matrix(matrix, n):
    """Splits a matrix."""
    splitted = np.split(matrix, n)
    return splitted


def reshape_elements(arr, shape):
    """reshaped every element in arr to shape"""

    reshaped = []
    for i in arr:
        shaped = i.reshape(shape)
        reshaped.append(shaped)
    return reshaped


def svd(matrix):
    """The svd."""

    matrix = np.nan_to_num(matrix)

    daskarr = dask.array.from_array(matrix)
    u, s, v = da.linalg.svd(daskarr)

    tonomap = u[:, 1] / math.sqrt(12)
    # plot_svd(u, s, v, name="First SVD")
    S = np.diag(s)
    k = 2

    tonomap = tonomap
    tonomap_computed = tonomap.compute()

    return tonomap_computed


def svd_and_save_images(beta_files, n_betas, n_samples, shape, affine, save_path):
    fdata_matrix = create_fdata_matrix(beta_files, n_betas)
    svd_matrix = svd(fdata_matrix)
    subjects = get_subjects_ordered(beta_files, n_betas)
    splitted = split_matrix(svd_matrix, n_samples)
    reshape = reshape_elements(splitted, shape)
    subjects_reshaped = zip(subjects, reshape)

    affine = np.load(affine)
    for i in subjects_reshaped:
        new_img = nb.Nifti1Image(i[1], affine)
        nb.save(new_img, f"{save_path}{i[0]}")
