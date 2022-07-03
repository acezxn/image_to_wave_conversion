# image sound conversion

The project is intended to convert images to sound, and convert sound to image

## how does it work?

### image to sound
The project converts an image into 2D arrays, and convert the 2D array to 1D by using the hilbert's curve. The brightness of the left down corner of a picture represents the amplitude of a low frequency, and the brightness of the right down corner of a picture represents the amplitude of a high frequency.

![image](https://github.com/acezxn/image_to_wave_conversion/blob/main/images/hilbert_curve.png)

After the 1D array is created, the project creates wave data with frequencies based on the data in the 1D array, the wave data then would be added together and exported as .wav file

![image](https://github.com/acezxn/image_to_wave_conversion/blob/main/pictures/B.jpg)
##### Original picture
![image](https://github.com/acezxn/image_to_wave_conversion/blob/main/audios/B.mp4)
##### Converted sound

### sound to image
The project performs fft on the wave data to get the frequency amplitude data of the sound, then based on the size of the image, the project averages the data from the fft output and make a low resolution version of the data (this is the data to write on the image), finally, the project uses the hilbert's curve to map back the 1D array data to 2D array and export the 2D array as an image

![image](https://github.com/acezxn/image_to_wave_conversion/blob/main/images/fft.png)
##### FFT result
![image](https://github.com/acezxn/image_to_wave_conversion/blob/main/images/convertedB.png)
##### Converted image
