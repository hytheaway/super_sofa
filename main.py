import numpy as np
import matplotlib.pyplot as plt
import sofa
import os

sofa_file_1 = input('sofa file 1: ')
sofa_file_2 = input('sofa file 2: ')
measurement = 0
emitter = 1
legend = []
print('measurement: ', measurement)
print('emitter: ', emitter)

SOFA_HRTF_1 = sofa.Database.open(sofa_file_1)
SOFA_HRTF_2 = sofa.Database.open(sofa_file_2)

for receiver in np.arange(SOFA_HRTF_1.Dimensions.R):
    legend.append('Receiver {0}'.format(receiver))
    
fig, ax = plt.subplots()

nfft_1 = len(SOFA_HRTF_1.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
HRTF_1 = np.fft.fft(SOFA_HRTF_1.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}),n=nfft_1, axis=0)
HRTF_mag_1 = (2/nfft_1)*np.abs(HRTF_1[0:int(len(HRTF_1)/2)+1])
HRTF_mag_dB_1 = 20*np.log10(HRTF_mag_1)
f_axis = np.linspace(0,(SOFA_HRTF_1.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2,len(HRTF_mag_dB_1))
plt.semilogx(f_axis, HRTF_mag_dB_1)


nfft_2 = len(SOFA_HRTF_2.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
HRTF_2 = np.fft.fft(SOFA_HRTF_2.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}),n=nfft_2, axis=0)
HRTF_mag_2 = (2/nfft_2)*np.abs(HRTF_2[0:int(len(HRTF_2)/2)+1])
HRTF_mag_dB_2 = 20*np.log10(HRTF_mag_2)
f_axis = np.linspace(0,(SOFA_HRTF_2.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2,len(HRTF_mag_dB_2))
plt.semilogx(f_axis, HRTF_mag_dB_2)
# ax = plt.gca()

plt.grid()
plt.grid(which='minor', color="0.9")
plt.title('{0}: HRTF at M={1} for emitter {2}'.format(os.path.basename(sofa_file_1), measurement, emitter))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend(['Left','Right'])

plt.figure(figsize=(15, 5))

plt.show()

SOFA_HRTF_1.close()
SOFA_HRTF_2.close()
plt.close()