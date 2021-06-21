import SimpleITK as sitk
import os, sys


def brain_normalization(input_img, outputDirectory): 
    input_img_nii = sitk.ReadImage(input_img, sitk.sitkFloat32)
    input_img_nor = sitk.Normalize(input_img_nii)
    sitk.WriteImage(input_img_nor, os.path.join(outputDirectory, input_img[:input_img.find('.')] + "_nml.nii"))
    print("Complete", input_img)
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        inputDirectory = sys.argv[1]
        outputDirectory = inputDirectory + "_normal"
        os.makedirs(outputDirectory)
        file_list = os.listdir(inputDirectory)

        for path in file_list:
            print(path)
            brain_normalization(os.path.join(inputDirectory, path), outputDirectory)
    else: 
        print("error")
        exit(0)