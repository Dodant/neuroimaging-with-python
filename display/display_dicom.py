import os, sys
import pydicom
import matplotlib.pyplot as plt

def display_dicom(): 
    
    X = []

    for _, dir, f in os.walk(folder_path):
        for filename in f:
            ds = pydicom.dcmread(folder_path + '\\' + filename)
            X.append(ds)

    window = plt.figure(figsize=(10,7))
    n_cols = 8
    n_rows = (len(X) // n_cols + 1)

    plt.title(folder_path[folder_path.rfind('\\')+1:])
    plt.axis("off")  
    for idx in range(0, len(X)):
        window.add_subplot(n_rows, n_cols, idx + 1)
        plt.axis("off")
        plt.imshow(X[idx].pixel_array, "gray")
    plt.show()
        

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2: 
            folder_path = sys.argv[1]
            display_dicom()
        else: 
            print("Enter DICOM file Directory");
            exit(1)
    except Exception as e:
        print('Error occured during execution-' + e)