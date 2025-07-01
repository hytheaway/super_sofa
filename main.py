import numpy as np
import matplotlib.pyplot as plt
import sofa
import os

sofa_file_1 = input('sofa file 1: ')
sofa_file_2 = input('sofa file 2: ')

# Hard-coded values for testing
measurement = 0
emitter = 1
legend = []
xlim = '20, 20000'
ylim = '-150, 0'

xlim = str(xlim)
for char in xlim:
    if char == '[' or char == ']' or char == ' ':
        xlim = xlim.replace(char, '')
for i in range(0, len(xlim)):
    if xlim[i] == ',':
        xlim_start = xlim[0:i]
        xlim_end = xlim[i+1:]

ylim = str(ylim)
for char in ylim:
    if char == '[' or char == ']' or char == ' ':
        ylim = ylim.replace(char, '')
for i in range(0, len(ylim)):
    if ylim[i] == ',':
        ylim_start = ylim[0:i]
        ylim_end = ylim[i+1:]

print('measurement: ', measurement)
print('emitter: ', emitter)

plt.figure(figsize=(15, 5))

SOFA_HRTF_1 = sofa.Database.open(sofa_file_1)
SOFA_HRTF_2 = sofa.Database.open(sofa_file_2)

for receiver in np.arange(SOFA_HRTF_1.Dimensions.R):
    legend.append('Receiver {0}'.format(receiver))

# Determine FFT length
nfft_1 = len(SOFA_HRTF_1.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
# Sets the length of the FFT to 8x the original IR length || Zero-padding for higher frequency resolution in the resulting FFT.

# Compute FFT of HRTF
HRTF_1 = np.fft.fft(SOFA_HRTF_1.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}),n=nfft_1, axis=0)
# nfft_1: newly-padded length for fft; axis=0: process the time-domain samples along the first dimension; HRTF_1 = complex-valued frequency domain representation.

# Calculate single-sided magnitude-spectrum
HRTF_mag_1 = (2/nfft_1)*np.abs(HRTF_1[0:int(len(HRTF_1)/2)+1])
# Takes the first half of the FFT (which is positive frequencies only), computes the magnitude using np.abs(), and scales by 2/nfft_1 to account for doubled energy in positive frequencies, and to normalize for FFT length. +1 to include both 0Hz (DC) and Nyquist/sampling frequency.

# Convert magnitude to decibels
HRTF_mag_dB_1 = 20*np.log10(HRTF_mag_1)
# Standard 20log10 formula for conversion from magnitude (linear) to decibels (logarithmic).

# Generate frequency axis
f_axis = np.linspace(0,(SOFA_HRTF_1.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2,len(HRTF_mag_dB_1))
# Bounds are from 0 (DC) - SamplingRate/2 (Nyquist frequency); length of the axis is equal to HRTF_mag_dB_1 so that there is 1 data point per possible grid point on the axis.

# Plots the frequency response
plt.semilogx(f_axis, HRTF_mag_dB_1)
# x-axis = f_axis (frequency); y-axis = HRTF_mag_dB_1 (decibels). 

nfft_2 = len(SOFA_HRTF_2.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
HRTF_2 = np.fft.fft(SOFA_HRTF_2.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}),n=nfft_2, axis=0)
HRTF_mag_2 = (2/nfft_2)*np.abs(HRTF_2[0:int(len(HRTF_2)/2)+1])
HRTF_mag_dB_2 = 20*np.log10(HRTF_mag_2)
f_axis = np.linspace(0,(SOFA_HRTF_2.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2,len(HRTF_mag_dB_2))
plt.semilogx(f_axis, HRTF_mag_dB_2)

ax = plt.gca() # Get whatever is splattered on the axes on the plot and assign that to ax (kind of the opposite of how this is normally done)
ax.set_xlim([int(xlim_start), int(xlim_end)]) # Bound the x-axis
ax.set_ylim([int(ylim_start), int(ylim_end)]) # Bound the y-axis
plt.grid() # Horizontal grid line
plt.grid(which='minor', color="0.9") # Vertical grid lines
plt.title('HRTF at M={0} for emitter {1}'.format(measurement, emitter))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend([os.path.basename(sofa_file_1),os.path.basename(sofa_file_2)])

plt.show()

SOFA_HRTF_1.close()
SOFA_HRTF_2.close()
plt.close()