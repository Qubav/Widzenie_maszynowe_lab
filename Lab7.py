from matplotlib.image import imread
import numpy as np
from matplotlib.pylab import plt
import os
import pywt


def fft_with_keeping(c_img: np.ndarray, keep) -> np.ndarray:
    Bt = np.fft.fft2(c_img)
    Btsort = np.sort(np.abs(Bt.reshape(-1)))
    # thresh = Btsort[int(np.floor((1-keep) * len(Btsort)))]
    mean = np.mean(Btsort) * 1.1
    thresh = mean

    # plt.figure()
    # plt.plot(Btsort)
    # plt.show()
    # thresh = np.max(Btsort)
    ind = np.abs(Bt) > thresh
    Atlow = Bt * ind
    Alow = np.fft.ifft2(Atlow).real
    Alow = np.clip(Alow, 0, 255).astype(np.uint8)
    Bt = Bt.real
    Bt = np.clip(Bt, 0, 255).astype(np.uint8)

    return Alow, Bt

def mae(img_Xo: np.ndarray, img_Xd: np.ndarray) -> float:

    n = img_Xd.shape[0] * img_Xd.shape[1] * 3
    suma = 0

    for c in range(3):
        for i in range(img_Xd.shape[0]):
            for j in range(img_Xd.shape[1]):
                suma += np.abs(img_Xo[i, j, c] - img_Xd[i, j, c])
    
    max_Xo = img_Xo.max()
    
    return suma / (n * max_Xo)



if __name__ == "__main__":
    plt.rcParams["figure.figsize"] = [5, 5]
    plt.rcParams.update({"font.size": 18})

    # A =  imread(os.path.join("panda.jpg"))
    A =  imread(os.path.join("circle.jpg"))
    # A =  imread(os.path.join("mond.jpg"))
    A_r = A[:, :, 0]
    A_g = A[:, :, 1]
    A_b = A[:, :, 2]
    A_components = [A_r, A_g, A_b]

    Fourier = True
    Wavelet = False

    # # FFT

    if Fourier is True:

        images_decompressed = []
        images_compressed = []

        plt.figure()
        plt.subplot(3, 1, 1)
        plt.imshow(A_r, cmap="gray")
        plt.subplot(3, 1, 2)
        plt.imshow(A_g, cmap="gray")
        plt.subplot(3, 1, 3)
        plt.imshow(A_b, cmap="gray")
        plt.axis("off")
        

        for keep in (0.1, 0.05, 0.01, 0.002):
            A_new  = []
            Bt_new = []
            for component in A_components:
                Alow, Bt = fft_with_keeping(component, keep)
                A_new.append(Alow)
                Bt_new.append(Bt)

            A_new_2 = np.dstack(A_new)
            Bt_new_2 = np.dstack(Bt_new)
            images_decompressed.append(A_new_2)
            images_compressed.append(Bt_new_2)
        
        for Alow in images_decompressed:
            plt.figure()
            plt.subplot(2,1, 1)
            plt.imshow(Alow, cmap="gray")
            plt.subplot(2, 1, 2)
            plt.imshow(Bt, cmap="gray")
            plt.axis("off")
            
        plt.show()

    # Wavelet

    if Wavelet is True:

        B = np.mean(A, -1)

        n = 4
        w = "db1"
        coeffs = pywt.wavedec2(B, wavelet = w, level = n)
        coeff_arr, coeffs_slices = pywt.coeffs_to_array(coeffs)

        Csort = np.sort(np.abs(coeff_arr.reshape(-1)))

        for keep in (0.1, 0.05, 0.01, 0.005):
            thresh = Csort[int(np.floor((1 - keep) * len(Csort)))]
            ind = np.abs(coeff_arr) > thresh
            Cfilt = coeff_arr * ind

            coeffs_filt = pywt.array_to_coeffs(Cfilt, coeffs_slices, output_format = 'wavedec2')
            Arecon = pywt.waverec2(coeffs_filt, wavelet = w)
            plt.figure()
            plt.imshow(Arecon.astype(np.uint8), cmap="gray")
            plt.axis("off")

            # czy to jest to compressed zdj?
            plt.figure()
            plt.imshow(np.clip(Cfilt, 0, 255).astype(np.uint8), cmap="gray")
            plt.show()
        
        plt.show()



    
    


