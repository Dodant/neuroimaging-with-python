import sys
import SimpleITK as sitk

def RegistrationImage(learningRate=0.1):

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

    sitk.WriteImage(moving_resampled, MOVING_IMAGE[:MOVING_IMAGE.find('.')] + "_RGSTRTN" + MOVING_IMAGE[MOVING_IMAGE.find('.'):])
    sitk.WriteTransform(final_transform, MOVING_IMAGE[:MOVING_IMAGE.find('.')] + "_TRNSFRM.tfm")


if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            #input file 
            FIXED_IMAGE = sys.argv[1]
            MOVING_IMAGE = sys.argv[2]
            RegistrationImage()
            print("Done")
        elif len(sys.argv) == 4:
            #input file 
            FIXED_IMAGE = sys.argv[1]
            MOVING_IMAGE = sys.argv[2]
            RegistrationImage(sys.argv[3])
            print("Done")
        else: 
            print("Enter Fixed img, Moving img, Learning Rate(optional)");
            exit(1)
    except Exception as e:
        print('Error occured during execution-' + e)