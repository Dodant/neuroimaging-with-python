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
here : [rotation/rotateimage.py](https://github.com/Dodant/neuroimaging-with-python/blob/main/rotation/rotateimage.py)   
Rotation Angle
- Positive value - anti-clockwise   
- Negative value - clockwise   
```shell
python rotation/rotateimage.py 'INPUT DIRECTORY' 'OUTPUT DIRECTORY' ROTATION-ANGLE
```   
### 2. Display Dicom Format
here : [display/display_dicom.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/display/display_dicom.ipynb)   
Run Jupyter Notebook and Change 'folder_path'   
### 3. Image Registration
here : [image_registration/image_registration.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/image_registration/image_registration.ipynb)   
**Input**
- Fixed Image (.nii, .mha, ...)
- Moving Image   

**Output**
- Moved Image
- Transformation File (.tfm)   
### 4. Smoothing



## References
- [InsightSoftwareConsortium/SimpleITK-Notebooks](https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks)
- [SuperElastix/SimpleElastix](https://github.com/SuperElastix/SimpleElastix)
- [voxelmorph/voxelmorph](https://github.com/voxelmorph/voxelmorph)
- [iitzco/deepbrain](https://github.com/iitzco/deepbrain)




## ETC
- [Download](http://nist.mni.mcgill.ca/?page_id=714) Brain Templates and Atlases here (MNI Space)
- [Download](https://www.microdicom.com/downloads.html) DICOM Viewer here (MicroDicom)  
- NIfTI Viewer : https://socr.umich.edu/HTML5/BrainViewer/
- DICOM to NIfTI
  ```shell
  pip install dcm2nii
  dcm2nii 'DICOM DIRECTORY'
  ```
