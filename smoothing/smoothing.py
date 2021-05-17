import sys
import nibabel as nib
import nibabel.processing

def SmoothingImage(sigma=3): 
    img = nib.load(input_img)
    fhwm = nib.processing.sigma2fwhm(sigma)
    smoothed_img = nib.processing.smooth_image(img, fhwm)
    nib.save(smoothed_img, input_img[:input_img.find('.')] + "_SMTH" + input_img[input_img.find('.'):])
    
if __name__ == "__main__": 
    try: 
        if len(sys.argv) == 2:
            input_img = sys.argv[1]
            SmoothingImage()
        elif len(sys.argv) == 3:
            input_img = sys.argv[1]
            sigma = int(sys.argv[2])
            SmoothingImage(sigma)
        else:            
            print("Enter input nii img, sigma(optional)");
            exit(1)
    except Exception as e:
        print('Error occured during execution-' + e)