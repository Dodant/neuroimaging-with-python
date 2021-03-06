import SimpleITK as sitk
import numpy as np
import os, sys
import nibabel as nib
import nibabel.processing
from pyrobex.robex import robex 

def AIO3(FIXED_IMAGE, MOVING_IMAGE, learningRate=1.0, sigma=3): 
    
    ## Registration
    fixed_image = sitk.ReadImage(FIXED_IMAGE, sitk.sitkFloat32)
    moving_image = sitk.ReadImage(MOVING_IMAGE, sitk.sitkFloat32)

    initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, 
                                                        sitk.Euler3DTransform(), 
                                                        sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)
    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=learningRate, 
                                                      numberOfIterations=100, 
                                                      convergenceMinimumValue=1e-6, 
                                                      convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.            
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4,2,1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)
    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32), 
                                                sitk.Cast(moving_image, sitk.sitkFloat32))

    print(f'Final metric value: {registration_method.GetMetricValue()}')
    print(f'Optimizer\'s stopping condition, {registration_method.GetOptimizerStopConditionDescription()}')

    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    RGSTRTN_IMAGE = MOVING_IMAGE[:MOVING_IMAGE.rfind('.')] + "_RGSTRTN" + MOVING_IMAGE[MOVING_IMAGE.rfind('.'):]
    print(type(moving_resampled), 'resample')
    sitk.WriteImage(moving_resampled, RGSTRTN_IMAGE)
    sitk.WriteTransform(final_transform, MOVING_IMAGE[:MOVING_IMAGE.rfind('.')] + "_TRNSFRM.tfm")


    ## Smoothing
    img = nib.load(RGSTRTN_IMAGE)
    fhwm = nib.processing.sigma2fwhm(sigma)
    smoothed_img = nib.processing.smooth_image(img, fhwm)
    SMTH_IMAGE = RGSTRTN_IMAGE[:RGSTRTN_IMAGE.rfind('.')] + "_SMTH" + RGSTRTN_IMAGE[RGSTRTN_IMAGE.rfind('.'):]
    print(type(smoothed_img), 'smooth')
    nib.save(smoothed_img, SMTH_IMAGE)


    ## Brain Extraction
    image = nib.load(SMTH_IMAGE)
    stripped, mask = robex(image)

    nib.save(stripped, os.path.dirname(SMTH_IMAGE) + '../stripped/' + os.path.basename(SMTH_IMAGE))
    nib.save(mask, os.path.dirname(SMTH_IMAGE) + '../mask/' + os.path.basename(SMTH_IMAGE))
    print(type(stripped), 'skipped')
    print(type(mask), 'mask')
    print("Complete", MOVING_IMAGE)
    


if __name__ == "__main__":
    print(123)
    if len(sys.argv) == 3:
        print(sys.argv)
        brain_template = sys.argv[1]
        folder_path = sys.argv[2]
        file_list = os.listdir(folder_path)
        file_list = [nii for nii in file_list if nii.endswith((".nii", ".nii.gz"))]
        print(file_list)
        for path in file_list:
            print(path)
            AIO3(brain_template, folder_path + "/" + path)
    else: 
        print("error")
        exit(0)