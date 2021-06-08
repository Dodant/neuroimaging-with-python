import dicom2nifti 
import pydicom as dcm
import os, sys

def convert_dcm_dir_to_nifti(sample):
    ds = dcm.read_file(os.path.join(sample, os.listdir(sample)[0]))
    outputfile = sample + '_' + ds.StudyDate
    dicom2nifti.dicom_series_to_nifti(sample, outputfile)
    print("Complete", outputfile)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        sample = sys.argv[1]
        convert_dcm_dir_to_nifti(sample)
    else: 
        print("input \'python dcm_to_nii_date.py \'DCM_DIRECTORY\'\'")
    