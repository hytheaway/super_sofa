import numpy as np
import matplotlib.pyplot as plt
import sofa
import os

sofa_file = input('sofa file: ')
measurement = 0
emitter = 1
legend = []
print('measurement: ', measurement)
print('emitter: ', emitter)

SOFA_HRTF = sofa.Database.open(sofa_file)

t = np.arange(0, SOFA_HRTF.Dimensions.N)*SOFA_HRTF.Data.SamplingRate.get_values(indices={"M":measurement})

for receiver in np.arange(SOFA_HRTF.Dimensions.R):
    legend.append('Receiver {0}'.format(receiver))

nfft = len(SOFA_HRTF.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))*8
HRTF = np.fft.fft(SOFA_HRTF.Data.IR.get_values(indices={"M":measurement, "R":receiver, "E":emitter}),n=nfft, axis=0)
HRTF_mag = (2/nfft)*np.abs(HRTF[0:int(len(HRTF)/2)+1])
HRTF_mag_dB = 20*np.log10(HRTF_mag)

plt.figure(figsize=(15, 5))
f_axis = np.linspace(0,(SOFA_HRTF.Data.SamplingRate.get_values(indices={"M":measurement, "R":receiver, "E":emitter}))/2,len(HRTF_mag_dB))
plt.semilogx(f_axis, HRTF_mag_dB)
ax = plt.gca()
plt.grid()
plt.grid(which='minor', color="0.9")
plt.title('{0}: HRTF at M={1} for emitter {2}'.format(os.path.basename(sofa_file), measurement, emitter))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend(['Left','Right'])
plt.show()

SOFA_HRTF.close()
plt.close()