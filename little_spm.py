import argparse
from argparse import RawTextHelpFormatter
import sys, os

from pyrobex.robex import robex
import SimpleITK as sitk
import nibabel as nib
import nibabel.processing
import dicom2nifti 
import pydicom as dcm
import imutils
import numpy as np
import cv2


def rotate_dicom_seires(inputDirectory, degOfRotation):
    dcmList = os.listdir(inputDirectory)
    outputDirectory = inputDirectory + "_rotated"
    os.makedirs(outputDirectory)
    
    for imgName in dcmList:
        path = os.path.join(inputDirectory, imgName)
        dcm = sitk.ReadImage(path)
        array = sitk.GetArrayFromImage(dcm)
        imgArray = array[0]
        rotate = imutils.rotate(imgArray, degOfRotation)
        filtered_image = sitk.GetImageFromArray(rotate)
        
        for key in dcm.GetMetaDataKeys():
            filtered_image.SetMetaData(key, dcm.GetMetaData(key))
        filtered_image.SetSpacing(dcm.GetSpacing())
        
        writer = sitk.ImageFileWriter()
        writer.KeepOriginalImageUIDOn()
        writer.SetFileName(os.path.join(outputDirectory, imgName))
        writer.Execute(filtered_image)
    print(inputDirectory +' saved successfully')

def convert_dcm_dir_to_nifti(inputDirectory): 
    dicom2nifti.dicom_series_to_nifti(inputDirectory, inputDirectory)
    print("Complete", inputDirectory)

def brain_smoothing(input_img, fwhm): 
    if not input_img.endswith(".nii"): 
        print("Input .nii file")
        exit(0)
    img = nib.load(input_img)
    smoothed_img = nib.processing.smooth_image(img, fwhm)
    nib.save(smoothed_img, input_img[:input_img.find('.')] + "_smth.nii")
    print("complete", input_img)

def brain_extraction(input_img):
    image = nib.load(input_img)
    stripped, mask = robex(image)
    nib.save(stripped, input_img + '_stripped.nii')
    nib.save(mask, input_img + '_mask.nii')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     'Little SPM Written in Python\n\n'\
                                     '1. Rotate Dicom Series\n'\
                                         '\tpython little_spm.py --rotate --directory \'SAMPLE DIRECTORY\' --angle ANGLE\n'\
                                         '\tex) python little_spm.py --rotate -d 15819775_T1 -a 3 \n\n'\
                                     '2. Convert Dicom to Nifti\n'\
                                         '\tpython little_spm.py --convert --directory \'SAMPLE DIRECTORY\'\n'\
                                         '\tex) python little_spm.py --convert -d 15819775_T1\n\n'\
                                     '3. Image Registration\n'\
                                         
                                     '4. Brain Smoothing\n'\
                                         '\tpython little_spm.py --smoothing --input \'NIFTI FILE\' --fwhm FWHM\n'\
                                         '\tex) python little_spm.py --smoothing -i 15819775_T1 -f 8\n\n'\
                                     '5. Brain Extraction\n'\
                                         '\tpython little_spm.py --extract --input \'NIFTI FILE\'\n'\
                                         '\tex) python little_spm.py --extract -i 15819775_T1\n\n'\
                                     '6. Normalization',
                                    epilog="Written by Dodant",
                                    formatter_class=RawTextHelpFormatter)

    #Rotate - Complete
    parser.add_argument('--rotate', 
                        action='store_true',
                        help='Rotate Dicom Series')
    parser.add_argument('-d', '--directory',
                        help='Single Sample Directory(Dicom Series)')
    parser.add_argument('-a', '--angle',
                        type=int, 
                        help='Rotation Angle: Positive Value - ACW / Negative Value - CW')
    
    #Dicom to Nifti - Complete
    parser.add_argument('--convert',
                        action='store_true',
                        help='Convert Sample(Dicom Series) to Nifti')

    #Image Registration - Work in Progress
    parser.add_argument('--registration',
                        action='store_true')
    parser.add_argument('-i', '--input',
                        help='Single Nifti File')
    parser.add_argument('-t', '--template', 
                        help='Fixed Brain Template for Registration',
                        choices=['t1','t2','pet','spect'], 
                        default='brain_atlas')
    
    #Brain Smoothing - Complete
    parser.add_argument('--smoothing',
                        action='store_true')
    parser.add_argument('-f', '--fwhm',
                        help="Full Width Half Max for Brain Smoothing",
                        type=int, default=6)

    #Brain Stripping - Complete
    parser.add_argument('--extract',
                        action='store_true',
                        help="Skill Stripping (Only run in Linux)")

    #Normalization - Work in Progress
    parser.add_argument('--normalization',
                        choices=['zscore','gmm','fcm','kde','ws'],
                        help=
                        "- Z-Score Normalization\n"\
                        "- Fuzzy C-means (FCM)-based tissue-based mean Normalization\n"\
                        "- Gaussian Mixture Model (GMM)-based WM mean Normalization\n"\
                        "- Kernel Density Estimate (KDE) WM mode Normalization\n"\
                        "- WhiteStripe")
    parser.add_argument('-m', '--mask',
                        help='Mask for Normalization')

    #ETC
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.rotate: 
        rotate_dicom_seires(args.directory, args.angle)
        
    if args.convert: 
        convert_dcm_dir_to_nifti(args.directory)
        
    if args.smoothing: 
        brain_smoothing(args.input, args.fwhm)
        
    if args.extract: 
        brain_extraction(args.input)