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

`pip install -r requirements.txt`

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

### 5. Normalization 
```shell
pip install intensity-normalization
```
#### Individual time-point normalization methods
- `zscore-normalize`: Z-score normalization 
   ```shell
   zsocre-normalize --image IMAGE --output-dir OUTPUT_DIR ([--brain-mask BRAIN_MASK] [--single-img])
   ```
- `fcm-normalize`: Fuzzy C-means (FCM)-based tissue-based mean normalization 
  ```shell
  fcm-normalize --image IMAGE --brain-mask BRAIN_MASK --tissue-mask TISSUE_MASK --output-dir OUTPUT_DIR ([--tissue-type {wm,gm,csf}] [--single-img])
  ```
- `gmm-normalize`: Gaussian Mixture Model (GMM)-based WM mean normalization 
  ```shell
  gmm-normalize --image IMAGE --brain-mask BRAIN_MASK --output-dir OUTPUT_DIR ([--contrast {t1,t2,flair}] [--single-img])
  ```
- `kde-normalize`: Kernel Density Estimate (KDE) WM mode normalization 
  ```shell
  kde-normalize --image IMAGE --brain-mask BRAIN_MASK ([--output-dir OUTPUT_DIR] [--contrast {t1,t2,flair,md, largest, first, last}] [--single-img])
  ```
- `ws-normalize`: WhiteStripe 
  ```shell
  ws-normalize --img-dir IMG_DIR --mask-dir MASK_DIR --output-dir OUTPUT-DIR ([--contrast {t1,t2,flair,md}])
  ```
#### Sample-based normalization methods
- `lsq-normalize`: Least squares (LSQ) tissue mean normalization 
  ```shell
  lsq-normalize --img-dir IMG_DIR --output-dir OUTPUT_DIR ([--mask-dir MASK_DIR])
  ```
- `nyul-normalize`: Piecewise Linear Histogram Matching (Nyúl & Udupa) 
  ```shell
  nyul-normalize --img-dir IMG_DIR --output-dir OUTPUT_DIR ([--mask-dir MASK_DIR])
  ```
- `ravel-normalize`: RAVEL 
  ```shell
  ravel-normalize --img-dir IMG_DIR --mask-dir MASK_DIR ([--output-dir OUTPUT_DIR] [--contrast {t1,t2,flair}])
  ```

### 6. Brain Extraction a.k.a. Skull-Stripping
[ROBEX](https://www.nitrc.org/projects/robex)(Robust Brain Extraction) for Linux (Windows is not supported)   
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
- Brain Extraction Tools
  - [HD-BET](https://github.com/MIC-DKFZ/HD-BET) for Linux   
    `hd-bet -i INPUT_FOLDER -o OUTPUT_FOLDER`
