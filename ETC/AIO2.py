import SimpleITK as sitk
import numpy as np
import os, sys
import nibabel as nib
import nibabel.processing

def AIO2(FIXED_IMAGE, MOVING_IMAGE, learningRate=0.1, sigma=3): 
    
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
    print(RGSTRTN_IMAGE)
    sitk.WriteImage(moving_resampled, RGSTRTN_IMAGE)
    sitk.WriteTransform(final_transform, MOVING_IMAGE[:MOVING_IMAGE.rfind('.')] + "_TRNSFRM.tfm")


    ## Smoothing
    img = nib.load(RGSTRTN_IMAGE)
    fhwm = nib.processing.sigma2fwhm(sigma)
    smoothed_img = nib.processing.smooth_image(img, fhwm)
    SMTH_IMAGE = RGSTRTN_IMAGE[:RGSTRTN_IMAGE.rfind('.')] + "_SMTH" + RGSTRTN_IMAGE[RGSTRTN_IMAGE.rfind('.'):]
    print(SMTH_IMAGE)
    nib.save(smoothed_img, SMTH_IMAGE)

AIO2('BRAIN_ATLAS.nii', 'CSY_72288349_FDG_PET.nii')


# if __name__ == "__main__":
#     if len(sys.argv) == 3:
#         brain_template = sys.argv[1]
#         path = sys.argv[2]
#         AIO2(brain_template, path)
#     else: 
#         print("error")
#         exit(0)