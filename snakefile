import numpy as np
import nibabel as nb
from scripts.nibabel_helper import *

configfile: "config.yaml"


rule all:
    input:
        "averaged_spmf/averaged_spmf.img",
        "averaged_spmf/affine.npy"


rule save_affine:
    input:
        get_spmf_files_as_list(config['tonotopy_data'])[0]
    output:
        config['affine']
    run:
        get_save_affine(input[0], output[0])


rule average_spmf:
    input:
        spmf_files = get_spmf_files_as_list(config['tonotopy_data'])
    output:
        config["averaged_spmf"]
    params:
        affine = np.load(config["affine"])
    run:
        save_average_spmf_file(input, params.affine, output[0])









