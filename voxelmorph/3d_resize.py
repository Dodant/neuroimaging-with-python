import numpy as np
import nibabel as nib
from scipy.ndimage import zoom

image_nib = nib.load("BRAIN_ATLAS_normal.nii")
image = image_nib.get_fdata()
resized_image = zoom(image, (160/image.shape[0], 192/image.shape[1], 224/image.shape[2]))
image_nifti = nib.Nifti1Image(resized_image, np.eye(4))
nib.save(image_nifti, "BRAIN_ATLAS_nrs.nii")
print("Complete", "BRAIN_ATLA_normalS.nii")