import numpy as np
import nibabel as nib
from scipy.ndimage import zoom

image_nib = nib.load("15819775_T1.nii")
image = image_nib.get_fdata()
resized_image = zoom(image, (160/image.shape[0], 192/image.shape[1], 224/image.shape[2]))
image_nifti = nib.Nifti1Image(resized_image, np.eye(4))
nib.save(image_nifti, "15819775_T1_resized.nii")
print("Complete", "15819775_T1.nii")