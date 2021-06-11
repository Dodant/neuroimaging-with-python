import os

sample_list = os.listdir('convert')
samples = [nii for nii in sample_list if nii.endswith(".nii")]
total_length = len(samples)
count = 0
for sample in samples:
    os.system(f"gmm-normalize -i convert/{sample} -m convert/mask/{sample} -o convert/normal/ -s")
    count += 1
    print(f"Count : {count} out of {total_length} - {round(count/total_length, 2)}%" )