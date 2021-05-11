# Neuroimaging with Python
 
## Format
- DICOM (.dcm) - Digital Imaging and Communications in Medicine
- NIfTI (.nii) - **Neuroimaging** Informatics Technology Initiative

## Library
- [**SimpleITK**](https://github.com/SimpleITK/SimpleITK) - Open Source Insight Segmentation and Registration Toolkit
- [Pydicom](https://github.com/pydicom/pydicom) - Python package for working with DICOM files 
- OpenCV - Open Source Computer Vision Library
- NumPy

## Feature
### 1. Rotate DICOM Format
Rotation Angle
- Positive value - anti-clockwise   
- Negative value - clockwise   
```python
python rotation/rotateimage.py 'INPUT DIRECTORY' 'OUTPUT DIRECTORY' ROTATION ANGLE
```

### 2. DICOM to NIfTI
```python
pip install dcm2nii
dcm2nii 'DICOM DIRECTORY'
```

### 3. Display Dicom Format
here : [display/display_dicom.ipynb](https://github.com/Dodant/neuroimaging-with-python/blob/main/display/display_dicom.ipynb)   
Run Jupyter Notebook and Change 'folder_path'


   
   
   
## ETC
- [Download](http://nist.mni.mcgill.ca/?page_id=714) Brain Templates and Atlases Here (MNI Space)
- [Download](https://www.microdicom.com/downloads.html) DICOM Viewer (MicroDicom)  
- NIfTI Viewer : https://socr.umich.edu/HTML5/BrainViewer/
