import SimpleITK as sitk
import sys, os
from pathlib import Path

def command_iteration(method):
    print(f"{method.GetOptimizerIteration():3} = {method.GetMetricValue():10.5f}")


if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "<movingImageFile> <fixedImageFilter> <numberOfIterations>")
    sys.exit(1)

fixed = sitk.ReadImage(sys.argv[2], sitk.sitkFloat32)
moving = sitk.ReadImage(sys.argv[1], sitk.sitkFloat32)

transformDomainMeshSize = [8] * moving.GetDimension()
tx = sitk.BSplineTransformInitializer(fixed, transformDomainMeshSize)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsCorrelation()
R.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=1e-5,
                       numberOfIterations=int(sys.argv[3]),
                       maximumNumberOfCorrections=5,
                       maximumNumberOfFunctionEvaluations=1000,
                       costFunctionConvergenceFactor=1e+7)
R.SetInitialTransform(tx, True)
R.SetInterpolator(sitk.sitkLinear)
R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R))

outTx = R.Execute(fixed, moving)

print("-------")
print(outTx)
print(f"Optimizer stop condition: {R.GetOptimizerStopConditionDescription()}")
print(f" Iteration: {R.GetOptimizerIteration()}")
print(f" Metric value: {R.GetMetricValue()}")

sitk.WriteTransform(outTx, sys.argv[3])

if ("SITK_NOSHOW" not in os.environ):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(100)
    resampler.SetTransform(outTx)

    out = resampler.Execute(moving)
    simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
    sitk.Show(cimg, "ImageRegistration1 Composition")
    
moving_resampled = sitk.Resample(moving, fixed, outTx, sitk.sitkLinear, 0.0, moving.GetPixelID())

sitk.WriteImage(moving_resampled, Path(sys.argv[1]).stem + "_re.nii")
sitk.WriteTransform(outTx, Path(sys.argv[1]).stem + "_tfm.tfm")
print("Complete", sys.argv[1])