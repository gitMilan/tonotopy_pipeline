import nibabel as nb


def load_nifti_image(path):
    nifti = nb.load(path)
    return nifti