import numpy as np
import nibabel as nb
from scripts.nibabel_helper import *
from scripts.svd_helper import *
from scripts.average_mapping import *
from scripts.plots import *
import os
import nibabel as nb

configfile: "config.yaml"

SAMPLES = os.listdir(config["tonotopy_data"])
subjects, betas = glob_wildcards(config["tonotopy_data"] + "/{subject}/Functional/lswzTask/{beta, (beta_)(\d+)}.img")
betas = list(dict.fromkeys(betas))


rule all:
    input:
        "plots/tonotopic_map.png"


rule save_affine:
    """Affine is a matrix which contains information about the 3D orientation of
        an fMRI scan, which is needed to create new nii-type images.
        As the affine is the same for all subjects, its useful to take
        a some affine from some subject and save it for later use"""
    input:
        get_spmf_files_as_list(config['tonotopy_data'])[0]
    output:
        "averaged_spmf/affine.npy"
    run:
        get_save_affine(input[0], output[0])


rule average_spmf:
    """The raw data contains voxels that may or may not be significant, an averaged spmf map
        is used for filtering significant voxels"""
    input:
        spmf_files = get_spmf_files_as_list(config['tonotopy_data']),
        affine = "averaged_spmf/affine.npy"
    output:
        "averaged_spmf/averaged_spmf.img"
    run:
        affine = np.load(input.affine)
        save_average_spmf_file(input.spmf_files, affine, output[0])


rule filter_significant_voxels:
    """Uses the functions in scripts/nibabel_helper.py to filter out the significant voxels"""
    input:
        betas = config["tonotopy_data"] + "{sample}/Functional/lswzTask/{beta}.img",
        average_spmf = "averaged_spmf/averaged_spmf.img"
    output:
        "filtered_betas/{sample}/{beta}.img"
    params:
        min_v = config["min_filter_value"]
    run:
        filter_significant_voxels(input[0], config["averaged_spmf"], params.min_v, output[0])


rule perform_svd:
    """Uses the significant voxels to perform a SVD, in which the second component describes the tonotopic maps
        This results in a large matrix which is then splitted into the tonotopic maps per subject."""
    input:
        expand("filtered_betas/{sample}/{beta}.img", sample=SAMPLES, beta=betas)
    output:
        expand("svd/{sample}.nii", sample=SAMPLES)
    params:
        n_betas = 12,
        n_samples = len(SAMPLES)
    run:
        shape = get_shape(input[0])
        svd_and_save_images(input, params.n_betas, params.n_samples, shape, config["affine"], config["svd_output"])


rule average_map:
    """Takes all tonotopic maps created by the (splitted) SVD and creates an averaged map of all of those"""
    input:
        tonotopic_maps = expand("svd/{sample}.nii", sample=SAMPLES),
        affine = "averaged_spmf/affine.npy"
    output:
        "average_map/averaged_map.nii"
    run:
        averaged_map = create_average_map(input.tonotopic_maps)
        affine = np.load(input.affine)
        save_nifti_image(averaged_map, affine, output[0])


rule plot_tonotopic_map:
    """Takes the averaged tonotopic map, which is an 3D image and creates
       a plot from the middle section using the start and stop params"""
    input:
        "average_map/averaged_map.nii"
    output:
        "plots/tonotopic_map.png"
    params:
        start=10,
        stop=28
    run:
        tonotopy_plot(input[0], params.start, params.stop, output[0])





