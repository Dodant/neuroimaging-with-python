# Neuroimaging with Python
 
## Formats
- DICOM (.dcm) - Digital Imaging and Communications in Medicine
- NIfTI (.nii) - **Neuroimaging** Informatics Technology Initiative

## Libraries
- [**SimpleITK**](https://github.com/SimpleITK/SimpleITK) - Open Source Insight Segmentation and Registration Toolkit
- [Pydicom](https://github.com/pydicom/pydicom) - Python package for working with DICOM files 
- OpenCV - Open Source Computer Vision Library
- NumPy

## Usage
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
[display/display_dicom.ipynb](https://github.com/)
Run Jupyter Notebook and Change 'folder_path'