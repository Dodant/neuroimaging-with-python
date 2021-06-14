import dicom2nifti 
import pydicom as dcm
import os, sys

def convert_dir_of_dcm_dirs_to_nifti(directory):
    for sample in os.listdir(directory):
        print(sample)
        convert_dcm_dir_to_nifti(directory, sample)

def convert_dcm_dir_to_nifti(directory, sample):
    ds = dcm.read_file(
            os.path.join(
                os.path.join(directory, sample), 
                os.listdir(os.path.join(directory, sample))[0])
        )
    print(ds.StudyDate)
    outputfile = sample + '_' + ds.StudyDate
    
    dicom2nifti.dicom_series_to_nifti(os.path.join(directory, sample), outputfile)
    print("Complete", outputfile)
    

if __name__ == "__main__":
    if len(sys.argv) == 2:
        DIR_OF_DCM_DIRS = sys.argv[1]
        convert_dir_of_dcm_dirs_to_nifti(DIR_OF_DCM_DIRS)
    else: 
        print("input \'python dcms_to_nii_date.py \'DIR_OF_DCM_DIRS\'\'")