import os, sys
import nibabel as nib
from pyrobex.robex import robex 

def skull_strip(input_img, stripped_path, mask_path):
    image = nib.load(input_img)
    stripped, mask = robex(image)

    nib.save(stripped, stripped_path)
    nib.save(mask, mask_path)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        path = sys.argv[1]
        file_list = os.listdir(path)
        file_list = [nii for nii in file_list if nii.endswith((".nii", ".nii.gz"))]
        for path in file_list:
            skull_strip(path, sys.argv[2], sys.argv[3])
    else: 
        print("please input img, stripped_path, mask_path")
        exit(0)