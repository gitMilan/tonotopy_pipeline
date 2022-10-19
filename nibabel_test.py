import nibabel as nb
import numpy as np

nifti_1 = "/home/milan/Documents/school/projects/tonotopy_pipeline/Tonotopy/con3810/Functional/lswzTask/spmF_0001.img"
nifti_2 = "/home/milan/Documents/school/projects/tonotopy_pipeline/Tonotopy/con3839/Functional/lswzTask/spmF_0001.img"

nb_load1 = nb.load(nifti_1)
nb_load2 = nb.load(nifti_2)

affine = nb_load1.affine

averaged_fdata = np.average([nb_load1.get_fdata(), nb_load2.get_fdata()], axis=3)

print(averaged_fdata)
