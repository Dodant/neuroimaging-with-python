import SimpleITK as sitk
import imutils
import os, sys
import numpy as np
import cv2

def RotateImage():
    """
    Input  - Dicom image
    Output - Dicom image
    It will rotate image by a specific angle provided by user.
    This function will accept 3 mandatory parameter 
    - source folder, 
    - destination folder, 
    - rotation-angle (positive value means anti-clockwise and negative value means clockwise rotation)
    """
    dcmList = os.listdir(inputDirectory)
    
    for imgName in dcmList:
        path = inputDirectory + '\\' + imgName
        dcm = sitk.ReadImage(path)
        array = sitk.GetArrayFromImage(dcm)
        imgArray = array[0] #sitk reads image as volume adding z-dimension
        rotate = imutils.rotate(imgArray, degOfRotation)
        filtered_image = sitk.GetImageFromArray(rotate)
        
        for key in dcm.GetMetaDataKeys():
            filtered_image.SetMetaData(key, dcm.GetMetaData(key))

        filtered_image.SetSpacing(dcm.GetSpacing())
        writer = sitk.ImageFileWriter()
        writer.KeepOriginalImageUIDOn()
        #writer
        writer.SetFileName(outputDiretory + '\\' + imgName)
        writer.Execute(filtered_image)
        print(imgName +' saved successfully')


if __name__ == '__main__':
    try:
        if len(sys.argv) < 4:
            print("Enter input path, output path, Degree of Rotation");
            exit(1)
        else:
            inputDirectory = sys.argv[1]
            outputDiretory = sys.argv[2]
            degOfRotation = int(sys.argv[3])
            RotateImage()
    except Exception as e:
        print('Error occured during execution-' + e)
        
"""
    author = "Dibya Raj Ghosh", 
    author_email = "dibyaraj11@gmail.com", 
    maintainer = "Dibya", 
    maintainer_email = "dibyaraj11@gmail.com", 
    description = "It will rotate image by a specific angle provided by user",
    long_description =
        Input  - Dicom image
        Output - Dicom image
        It will rotate image by a specific angle provided by user.
        This function will accept 3 mandatory parameter 
        - source folder, 
        - destination folder, 
        - rotation-angle (positive value means anticlockwise and negative value means clockwise rotation), 
    license="MIT"
"""