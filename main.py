import numpy as np
import matplotlib.pyplot as plt
import sofa
import os

input_sofa_files = input('List paths to all .sofa files to be used here (separated by comma): ')

# Clean up input
sofa_files_list = input_sofa_files.split(",")
sofa_files_list = [file.strip(' ') for file in sofa_files_list]

print('Number of SOFA files:', len(sofa_files_list))

# Hard-coded values for testing
measurement = 0
emitter = 1
receiver_legend = []
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

plt.figure(figsize=(15, 5), num=str('Left-Channel Head-Related Transfer Function Comparison'))

for i in sofa_files_list:
    legend.append(os.path.basename(i))
    SOFA_HRTF = sofa.Database.open(i)
    
    for receiver in np.arange(SOFA_HRTF.Dimensions.R):
        receiver_legend.append('Receiver {0}'.format(receiver))
        
    # Determine FFT length
    nfft = len(SOFA_HRTF.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
    # Sets the length of the FFT to 8x the original IR length || Zero-padding for higher frequency resolution in the resulting FFT.
    
    # Compute FFT of HRTF
    HRTF = np.fft.fft(SOFA_HRTF.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}), n=nfft, axis=0)
    # nfft: newly-padded length for fft; axis=0: process the time-domain samples along the first dimension; HRTF = complex-valued frequency domain representation.
    
    # Calculate single-sided magnitude-spectrum
    HRTF_mag = (2/nfft)*np.abs(HRTF[0:int(len(HRTF)/2)+1])
    # Takes the first half of the FFT (which is positive frequencies only), computes the magnitude using np.abs(), and scales by 2/nfft to account for doubled energy in positive frequencies, and to normalize for FFT length. +1 to include both 0Hz (DC) and Nyquist/sampling frequency.
    
    # Convert magnitude to decibels
    HRTF_mag_dB = 20*np.log10(HRTF_mag)
    # Standard 20log10 formula for conversion from magnitude (linear) to decibels (logarithmic).
    
    # Generate frequency axis
    f_axis = np.linspace(0, (SOFA_HRTF.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2, len(HRTF_mag_dB))
    # Bounds are from 0 (DC) - SamplingRate/2 (Nyquist frequency); length of the axis is equal to HRTF_mag_dB so that there is 1 data point per possible grid point on the axis.
    
    # Plots the frequency response
    plt.semilogx(f_axis, HRTF_mag_dB)
    # x-axis = f_axis (frequency); y-axis = HRTF_mag_dB (decibels). 
    
    SOFA_HRTF.close()

ax = plt.gca() # Get whatever is splattered on the axes on the plot and assign that to ax (kind of the opposite of how this is normally done)
ax.set_xlim([int(xlim_start), int(xlim_end)]) # Bound the x-axis
ax.set_ylim([int(ylim_start), int(ylim_end)]) # Bound the y-axis
plt.grid() # Horizontal grid line
plt.grid(which='minor', color="0.9") # Vertical grid lines
plt.title('Left-Channel HRTF Comparison at M={0} for emitter {1}'.format(measurement, emitter))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend(legend)

plt.show()

plt.close()