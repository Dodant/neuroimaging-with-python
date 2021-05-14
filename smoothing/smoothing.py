import sys
import nibabel as nib
import nibabel.processing

def SmoothingImage(sigma=3): 
    img = nib.load(input_img)
    fhwm = nib.processing.sigma2fwhm(sigma)
    smoothed_img = nib.processing.smooth_image(img, fhwm)
    nib.save(smoothed_img, saved_img)
    
if __name__ == "__main__": 
    try: 
        if len(sys.argv) == 3:
            input_img = sys.argv[1]
            saved_img = sys.argv[2]
            SmoothingImage()
        elif len(sys.argv) == 4:
            input_img = sys.argv[1]
            saved_img = sys.argv[2]
            sigma = int(sys.argv[3])
            SmoothingImage(sigma)
        else:            
            print("Enter input nii img, output nii img, sigma");
            exit(1)
    except Exception as e:
        print('Error occured during execution-' + e)