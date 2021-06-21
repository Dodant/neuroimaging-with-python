import SimpleITK as sitk 

input_img = "BRAIN_ATLAS_normal_resized.nii"
input_img_load =  sitk.ReadImage(input_img, sitk.sitkFloat32)
new_images = sitk.AdaptiveHistogramEqualization(input_img_load)
sitk.WriteImage(new_images, "BRAIN_ATLAS_hist.nii")
print("Complete", input_img)