# Neuroimaging with Python
 
## Format
- DICOM (.dcm) - Digital Imaging and Communications in Medicine
- NIfTI (.nii) - **Neuroimaging** Informatics Technology Initiative

## Requirements
- [**SimpleITK**](https://github.com/SimpleITK/SimpleITK) - Open Source Insight Segmentation and Registration Toolkit
- [Pydicom](https://github.com/pydicom/pydicom) - Python package for working with DICOM files 
- [Nibabel](https://nipy.org/nibabel/#) - Successor of PyNIfTI
- OpenCV - Open Source Computer Vision Library
- NumPy

## Feature
### 1. Rotate DICOM Format
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

### 3. Image Registration
here : [image_registration/image_registration.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/image_registration/image_registration.ipynb)   
**Input** - Fixed Image & Moving Image (.nii, .mha, ...)   
**Output** - Moved Image & Transformation File (.tfm)   
or
```shell
python image_registration/image_registration.py 'FIXED IMAGE' 'MOVING IMAGE' LearningRate(optional)
```
### 4. Smoothing
here : [smoothing/smoothing.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/smoothing/smoothing.ipynb)   
**Input** - NIfTI Image (.nii)   
**Output** - Smoothed Image (.nii)   
or
```shell
python smoothing/smoothing.py 'INPUT NIfTI' 'OUTPUT NIfTI' SIGMA(optional)
```   

### 5. Normalization (Work in Progress)   


## References
- [InsightSoftwareConsortium/SimpleITK-Notebooks](https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks)
- [SuperElastix/SimpleElastix](https://github.com/SuperElastix/SimpleElastix)
- [voxelmorph/voxelmorph](https://github.com/voxelmorph/voxelmorph)
- [iitzco/deepbrain](https://github.com/iitzco/deepbrain)
- [ANTsX/ANTsPy](https://github.com/ANTsX/ANTsPy)


## ETC
- [Download](http://nist.mni.mcgill.ca/?page_id=714) Brain Templates and Atlases here (MNI Space)
- [Download](https://www.microdicom.com/downloads.html) DICOM Viewer here (MicroDicom)  
- [Download](https://nifti-to-dicom.en.softonic.com/) NIfTI to DICOM here
- NIfTI Viewer : https://socr.umich.edu/HTML5/BrainViewer/
- DICOM to NIfTI
  ```shell
  pip install dcm2nii
  dcm2nii 'DICOM DIRECTORY'
  ```
- DICOM or NIfTI to JPEG or PNG
   ```shell
   pip install med2image
   med2image -i 'INPUT DICOM OR NIfTI' -d 'OUTPUT DIRECTORY`
   ```
- Brain Extraction Tools (a.k.a Skull-Stripping)
  - [ROBEX](https://www.nitrc.org/projects/robex)(Robust Brain Extraction) for Linux (Windows is not supported)   
  or   
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
  - [HD-BET](https://github.com/MIC-DKFZ/HD-BET) for Linux   
    `hd-bet -i INPUT_FOLDER -o OUTPUT_FOLDER`
