import argparse
import os, sys
from argparse import RawTextHelpFormatter

import cv2
import dicom2nifti
import imutils
import nibabel as nib
import nibabel.processing
from pathlib import Path
import numpy as np
import pydicom as dcm
import SimpleITK as sitk
from pyrobex.robex import robex
from scipy.ndimage import zoom


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
    print(inputDirectory, 'saved successfully')

def convert_dcm_dir_to_nifti(inputDirectory): 
    dicom2nifti.dicom_series_to_nifti(inputDirectory, inputDirectory)
    print("Complete", inputDirectory)

def voxel_2d(input_img, template):
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    os.system(f'python ./voxelmorph/scripts/tf/register.py --moving {input_img} --fixed {template} --moved {input_img}_v2.nii --model ./voxelmorph/model/brain_2D_smooth.h5')
    print("Complete", input_img)

def voxel_3d(input_img, template):
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    os.system(f'python ./voxelmorph/scripts/tf/register.py --moving {input_img} --fixed {template} --moved {input_img}_v3.nii --model ./voxelmorph/model/brain_3D.h5')
    print("Complete", input_img)
    
def brain_smoothing(input_img, fwhm): 
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    img = nib.load(input_img)
    smoothed_img = nib.processing.smooth_image(img, fwhm)
    nib.save(smoothed_img, Path(input_img).stem + "_smth.nii")
    print("Complete", input_img)

def brain_extraction(input_img):
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    image = nib.load(input_img)
    stripped, mask = robex(image)
    nib.save(stripped, Path(input_img).stem + '_stripped.nii')
    nib.save(mask, Path(input_img).stem + '_mask.nii')
    print("Complete", input_img)

def brain_normalization(input_img):
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    input_img_nii = sitk.ReadImage(input_img, sitk.sitkFloat32)
    input_img_nor = sitk.Normalize(input_img_nii)
    sitk.WriteImage(input_img_nor, Path(input_img).stem + "_normal.nii")
    print("Complete", input_img)

def brain_resize(input_img, x, y, z):
    if not os.path.splitext(input_img)[1] == "nii": 
        print("Input .nii file")
        exit(0)
    image_nib = nib.load(input_img).get_fdata()
    resized_image = zoom(image_nib, (x/image_nib.shape[0], y/image_nib.shape[1], z/image_nib.shape[2]))
    image_nifti = nib.Nifti1Image(resized_image, np.eye(4))
    nib.save(image_nifti, Path(input_img).stem + "_resize.nii")
    print("Complete", input_img)
    
    
# def flow(input_img, template): 
    # input nifti file 
    
    # normalization 
    # resize 
    # image registration 
    # smoothing

    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     'Little SPM Written in Python\n\n'\
                                     '1. Rotate Dicom Series\n'\
                                         '\tpython little_spm.py --rotate --directory <sample directory> --angle <degree>\n'\
                                         '\tex) python little_spm.py --rotate -d 15819775_T1 -a 3 \n\n'\
                                     '2. Convert Dicom to Nifti\n'\
                                         '\tpython little_spm.py --convert --directory <sample directory>\n'\
                                         '\tex) python little_spm.py --convert -d 15819775_T1\n\n'\
                                     '3. Image Registration\n'\
                                         '\tVoxel 2D'\
                                         '\tpython little_spm.py --registration --dimension 2 --input <dicom image> --fixed <dicom image>\n'\
                                         '\tex) python little_spm.py --registration --dimension 2 -i 15819775_T1_12.dcm --fixed fixed_image.dcm\n\n'\
                                         '\tVoxel 3D'\
                                         '\tpython little_spm.py --registration --dimension 3 --input <nifti file> --template <brain atlas>\n'\
                                         '\tex) python little_spm.py --registration -i 15819775_T1.nii -t t1\n\n'\
                                     '4. Brain Smoothing\n'\
                                         '\tpython little_spm.py --smoothing --input <nifti file> --fwhm <fwhm>\n'\
                                         '\tex) python little_spm.py --smoothing -i 15819775_T1.nii -f 8\n\n'\
                                     '5. Brain Extraction (Only run in Linux)\n'\
                                         '\tpython little_spm.py --extract --input <nifti file>\n'\
                                         '\tex) python little_spm.py --extract -i 15819775_T1.nii\n\n'\
                                     '6. Normalization\n'\
                                         '\tpython little_spm.py --normalize --input <nifti file>\n'\
                                         '\tex) python little_spm.py --normalize -i 15819775_T1.nii\n\n'\
                                     '7. Resize\n'\
                                         '\tpython little_spm.py --resize --input <nifti file> -x <x> -y <y> -z <z>\n'\
                                         '\tex) python little_spm.py --normalize -i 15819775_T1.nii -x 160 -y 190 -z 224\n\n',
                                    epilog="Written by Dodant",
                                    formatter_class=RawTextHelpFormatter)

    #Rotate
    parser.add_argument('--rotate', 
                        action='store_true',
                        help='Rotate Dicom Series')
    parser.add_argument('-d', '--directory',
                        help='Single Sample Directory(Dicom Series)')
    parser.add_argument('-a', '--angle',
                        type=int, 
                        help='Rotation Angle: Positive Value - ACW / Negative Value - CW')
    
    #Dicom to Nifti
    parser.add_argument('--convert',
                        action='store_true',
                        help='Convert Sample(Dicom Series) to Nifti')

    #Image Registration
    parser.add_argument('--registration',
                        action='store_true')
    parser.add_argument('--dimension',
                        type=int,
                        choices=[2,3],
                        default=3)
    parser.add_argument('--fixed')
    parser.add_argument('-i', '--input',
                        help='Single Nifti File')
    parser.add_argument('-t', '--template', 
                        help='Fixed Brain Template for Registration',
                        choices=['t1','t2','pet','spect'], 
                        default='brain_atlas')
    
    #Brain Smoothing
    parser.add_argument('--smoothing',
                        action='store_true')
    parser.add_argument('-f', '--fwhm',
                        help="Full Width Half Max for Brain Smoothing",
                        type=int, default=6)

    #Brain Stripping
    parser.add_argument('--extract',
                        action='store_true',
                        help="Skill Stripping")

    #Normalization
    parser.add_argument('--normalize',
                        action='store_true')

    #Resize 
    parser.add_argument('--resize',
                        action='store_true')
    parser.add_argument('-x', default=160)
    parser.add_argument('-y', default=192)
    parser.add_argument('-z', default=224)

    #ETC
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.2')
    args = parser.parse_args()

    if args.rotate: 
        rotate_dicom_seires(args.directory, args.angle)
        
    if args.convert: 
        convert_dcm_dir_to_nifti(args.directory)
        
    if args.registration: 
        if args.dimension == 2: 
            voxel_2d(args.input, args.fixed)
        else:
            if args.template == 'brain_atlas' or 'pet' or 'spect': 
                temp = "voxelmorph/templates/mni_icbm152_t1_tal_nlin_sym_09a_nml.nii"
            elif args.template == 't1':
                temp = "voxelmorph/templates/mni_icbm152_t1_tal_nlin_sym_09c_nml.nii"
            elif args.template == 't2':
                temp = "voxelmorph/templates/mni_icbm152_t2_tal_nlin_sym_09c_nml.nii"
            voxel_3d(args.input, temp)

    if args.smoothing: 
        brain_smoothing(args.input, args.fwhm)
        
    if args.extract: 
        brain_extraction(args.input)
        
    if args.normalize:
        brain_normalization(args.input)
        
    if args.resize:
        brain_resize(args.input, args.x, args.y, args.z)