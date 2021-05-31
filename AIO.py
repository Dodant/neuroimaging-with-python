import SimpleITK as sitk
import numpy as np
import os, sys
import nibabel as nib
from pyrobex.robex import robex 

def AIO(FIXED_IMAGE, MOVING_IMAGE, learningRate=0.1, sigma=3): 
    
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

    RGSTRTN_IMAGE = MOVING_IMAGE[:MOVING_IMAGE.find('.')] + "_RGSTRTN" + MOVING_IMAGE[MOVING_IMAGE.find('.'):]
    sitk.WriteImage(moving_resampled, RGSTRTN_IMAGE)
    sitk.WriteTransform(final_transform, MOVING_IMAGE[:MOVING_IMAGE.find('.')] + "_TRNSFRM.tfm")


    ## Smoothing
    img = nib.load(RGSTRTN_IMAGE)
    fhwm = nib.processing.sigma2fwhm(sigma)
    smoothed_img = nib.processing.smooth_image(img, fhwm)
    SMTH_IMAGE = RGSTRTN_IMAGE[:RGSTRTN_IMAGE.find('.')] + "_SMTH" + RGSTRTN_IMAGE[RGSTRTN_IMAGE.find('.'):]
    nib.save(smoothed_img, SMTH_IMAGE)


    ## Brain Extraction
    image = nib.load(SMTH_IMAGE)
    stripped, mask = robex(image)

    nib.save(stripped, os.path.dirname(SMTH_IMAGE) + '../stripped/' + os.path.basename(SMTH_IMAGE))
    nib.save(mask, os.path.dirname(SMTH_IMAGE) + '../mask/' + os.path.basename(SMTH_IMAGE))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        brain_template = sys.argv[1]
        path = sys.argv[2]
        file_list = os.listdir(path)
        file_list = [nii for nii in file_list if nii.endswith((".nii", ".nii.gz"))]
        for path in file_list:
            AIO(brain_template, path)
    else: 
        print("error")
        exit(0)