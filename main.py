import numpy as np

fs = 48000                                  # sampling rate
f = 1000                                    # frequency of 'actual signal'

t = np.arange(0, 0.01, 1/fs)                # time array
print(t)
signal = np.sign(np.sin(2*np.pi*f*t))       # amplited/signal value
print(signal)

# With 'noise'
noise = np.random.normal(0, 0.05, len(signal))
noisy_signal = signal + noise

# Modulation - Map bits to symbols, multiply 
# onto a carrier (numpy — generate a carrier 
# at some frequency, phase-shift by 0/π for 
# BPSK or 0/π/2/π/3π/2 for QPSK), sum, output 
# as the "transmitted" signal.

    #BPSK
        # bit 0 - pi degree modulation phase | multiply by -1 since inverted sine wave
        # 1 - 0 degree modulation phase

    #QPSK

# Demodulation


# Verification
