# Neuroimaging with Python
 
## Formats
- DICOM (.dcm) - Digital Imaging and Communications in Medicine
- NIfTI (.nii) - **Neuroimaging** Informatics Technology Initiative

## Libraries
- **SimpleITK** - Open Source Insight Segmentation and Registration Toolkit
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
pip install dic2nii
dcm2nii 'DICOM DIRECTORY'
```
