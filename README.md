# Neuroimaging with Python
 
## Overview
Make It Possible Fundamental SPM Features in Python

## Table of Contents
- [Format](#format)
- [Requirements](#requirements)
- [Feature](#feature)
   + [Rotate DICOM Format](#1-rotate-dicom-format)
   + [Display Dicom Format](#2-display-dicom-format)
   + [DICOM to NIFTI](#3-dicom-to-nifti)
   + [Image Registration](#4-image-registration)
   + [Smoothing](#5-smoothing)
   + [Normalization](#6-normalization)
   + [Brain Extraction](#7-brain-extraction-aka-skull-stripping)
   + Brain Resize
- [Little SPM Manual](little-spm-manual)
- [References](#references)
- [Tips](#tips)
 
## Format
- DICOM (.dcm) - Digital Imaging and Communications in Medicine
- NIfTI (.nii) - **Neuroimaging** Informatics Technology Initiative

## Requirements
- [**SimpleITK**](https://github.com/SimpleITK/SimpleITK) - Open Source Insight Segmentation and Registration Toolkit
- [Pydicom](https://github.com/pydicom/pydicom) - Python package for working with DICOM files 
- [Nibabel](https://nipy.org/nibabel/#) - Successor of PyNIfTI
- [dicom2nifti](https://github.com/icometrix/dicom2nifti) - Python library for converting dicom files to nifti
- OpenCV - Open Source Computer Vision Library
- NumPy   

`pip install -r requirements.txt`

## Feature
### 1. Rotate Dicom Format
here : [rotation/rotate_image.py](https://github.com/Dodant/neuroimaging-with-python/blob/main/rotation/rotate_image.py)   
Rotation Angle - Positive(+) value - ACW / Negative(-) value - CW   
```shell
python rotation/rotateimage.py 'INPUT DIRECTORY' 'OUTPUT DIRECTORY' ROTATION-ANGLE
```   

### 2. Display Dicom Format
here : [display/display_dicom.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/display/display_dicom.ipynb)   
Run Jupyter Notebook and Change 'folder_path'   
or
```shell
python display/display_dicom.py 'DICOM FOLDER PATH'
```

### 3. DICOM to NIFTI
for handling single sample
```shell
python dcm_to_nii_date.py 'SAMPLE_FOLDER'
```
for handling multiple samples
```shell
python dcms_to_nii_date.py 'DIRECTORY_OF_DICOM_SAMPLES'
```


### 4. Image Registration
here : [image_registration/image_registration.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/image_registration/image_registration.ipynb)   
**Input** - Fixed Image & Moving Image (.nii, .mha, ...)   
**Output** - Moved Image & Transformation File (.tfm)   
or
```shell
python image_registration/image_registration_BS.py 'MOVING IMAGE' 'FIXED IMAGE' 
```

### 5. Smoothing
here : [smoothing/smoothing.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/smoothing/smoothing.ipynb)   
**Input** - NIfTI Image (.nii)   
**Output** - Smoothed Image (.nii)   
or
```shell
python smoothing/smoothing.py 'INPUT NIfTI' 'OUTPUT NIfTI' SIGMA(optional)
```   

### 6. Normalization
```shell
pip install intensity-normalization
```
#### Individual time-point normalization methods
```shell
# Z-score normalization   
zsocre-normalize --image IMAGE --output-dir OUTPUT_DIR ([--brain-mask BRAIN_MASK] [--single-img])
# Fuzzy C-means (FCM)-based tissue-based mean normalization  
fcm-normalize --image IMAGE --brain-mask BRAIN_MASK --tissue-mask TISSUE_MASK --output-dir OUTPUT_DIR ([--tissue-type {wm,gm,csf}] [--single-img])
# Gaussian Mixture Model (GMM)-based WM mean normalization   
gmm-normalize --image IMAGE --brain-mask BRAIN_MASK --output-dir OUTPUT_DIR ([--contrast {t1,t2,flair}] [--single-img])
# Kernel Density Estimate (KDE) WM mode normalization   
kde-normalize --image IMAGE --brain-mask BRAIN_MASK ([--output-dir OUTPUT_DIR] [--contrast {t1,t2,flair,md,largest,first,last}] [--single-img])
# WhiteStripe   
ws-normalize --img-dir IMG_DIR --mask-dir MASK_DIR --output-dir OUTPUT-DIR ([--contrast {t1,t2,flair,md}])
```
#### Sample-based normalization methods
```shell
# Least squares (LSQ) tissue mean normalization   
lsq-normalize --img-dir IMG_DIR --output-dir OUTPUT_DIR ([--mask-dir MASK_DIR])
# Piecewise Linear Histogram Matching (Nyúl & Udupa)   
nyul-normalize --img-dir IMG_DIR --output-dir OUTPUT_DIR ([--mask-dir MASK_DIR])
# RAVEL   
ravel-normalize --img-dir IMG_DIR --mask-dir MASK_DIR ([--output-dir OUTPUT_DIR] [--contrast {t1,t2,flair}])
```
### 7. Brain Extraction a.k.a. Skull-Stripping
[ROBEX](https://www.nitrc.org/projects/robex)(Robust Brain Extraction) for Linux (Windows is not supported)   
```shell
pip install pyrobex
robex path/to/t1w_image.nii -os path/to/stripped.nii -om path/to/mask.nii
```
```python
import nibabel as nib
from pyrobex.robex import robex
image = nib.load('path/to/t1w_image.nii')
stripped, mask = robex(image)
```
#### Multi Stripping
```shell
python multi_brain_extraction.py path/to/original -os path/to/stripped -om path/to/mask
```

## Little SPM Manual
Input Folder
- Dicom to Nifti   
	`python little_spm.py --rotate --directory <sample directory> --angle <degree>`   
	`ex) python little_spm.py --rotate -d 15819775_T1 -a 3`

- Rotate Dicoms   
	`python little_spm.py --convert --directory <sample directory>`   
	`ex) python little_spm.py --convert -d 15819775_T1`

Input Nifti
- Image Registration   
	`python little_spm.py --registration --input <dicom image> --template <dicom image> --iterations <numberOfIterations>`   
	`ex) python little_spm.py --registration -i 15819775.nii -t brain_atlas.nii`

- Brain Smoothing   
	`python little_spm.py --smoothing --input <nifti file> --fwhm <fwhm>`   
	`ex) python little_spm.py --smoothing -i 15819775_T1.nii -f 8`

- Brain Extraction (Only run in Linux)   
	`python little_spm.py --extract --input <nifti file>`   
	`ex) python little_spm.py --extract -i 15819775_T1.nii`

- Normalization   
	`python little_spm.py --normalize --input <nifti file>`   
	`ex) python little_spm.py --normalize -i 15819775_T1.nii`

- Resize   
	`python little_spm.py --resize --input <nifti file> -x <x> -y <y> -z <z>`   
	`ex) python little_spm.py --normalize -i 15819775_T1.nii -x 160 -y 190 -z 224`





## References
- Image Registraion
  - [InsightSoftwareConsortium/SimpleITK-Notebooks](https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks)
  - [SuperElastix/SimpleElastix](https://github.com/SuperElastix/SimpleElastix)
  - [voxelmorph/voxelmorph](https://github.com/voxelmorph/voxelmorph)
- Brain Extraction
  - [iitzco/deepbrain](https://github.com/iitzco/deepbrain)
- Normalization
  - [ANTsX/ANTsPy](https://github.com/ANTsX/ANTsPy)
  - [jcreinhold/intensity-normalization](https://github.com/jcreinhold/intensity-normalization)
  - [sergivalverde/MRI_intensity_normalization](https://github.com/sergivalverde/MRI_intensity_normalization)


## Tips
- [Download](http://nist.mni.mcgill.ca/?page_id=714) Brain Templates and Atlases here (MNI Space)
- [Download](https://www.microdicom.com/downloads.html) DICOM Viewer here (MicroDicom)  
- [Download](https://nifti-to-dicom.en.softonic.com/) NIfTI to DICOM here
- [Download](https://xmedcon.sourceforge.io/) (X)MedCon - Open Source Toolkit for Medical Image Conversion
- NIfTI Viewer : https://socr.umich.edu/HTML5/BrainViewer/
- DICOM or NIfTI to JPEG or PNG
   ```shell
   pip install med2image
   med2image -i 'INPUT DICOM OR NIfTI' -d 'OUTPUT DIRECTORY`
   ```
- Brain Extraction Tools
  - [HD-BET](https://github.com/MIC-DKFZ/HD-BET) for Linux   
    `hd-bet -i INPUT_FOLDER -o OUTPUT_FOLDER`
