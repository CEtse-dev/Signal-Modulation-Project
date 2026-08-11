import numpy as np

fs = 40                                  # sampling rate []
f = 1000                                    # frequency of 'actual signal'

fc = 4000                                   # carrier frequency (Hz) 
# fc must be less than fs/2 (NyQuist)
# fc must be more than actual signal frequency

bit_rate = 10

samples_per_bit = int(fs / bit_rate)

bits = np.array([0, 1, 1, 0])               # message

print("INPUT BITS: ", bits, "\n")

symbols = (bits*2) - 1                      # 0 => -1; 1 => 1

print("Symbols: ", symbols)

signal = np.repeat(symbols, samples_per_bit)         # symbols // signal

print("Signal(symbols): ", signal, "\n")

t = np.arange(len(signal)) / fs + 1e-3
print("Time stamps: ", t)

# With 'noise'
noise = np.random.normal(0, 0.1, len(signal))
noisy_signal = signal + noise

#signal = noisy_signal                              #--> includes noise as needed

# filtering

    # signal variable treated as symbols for bits

# Modulation

carrier = np.sin(2*np.pi*fc*t)
carrier_cos = np.cos(2*np.pi*fc*t)

    #BPSK
        # bit 0 - pi degree modulation phase | same as multiply by -1
        # 1 - 0 degree modulation phase

bpsk_signal = carrier * signal

print("BPSK Signal: ", bpsk_signal)

    #QPSK --> the same just orthogonal
I = signal
Q = np.sign(np.cos(2*np.pi*f*t))            # Q is simply orthogonal; +pi/2 or cos

# ^ also works np.sign(np.sin(2*np.pi*f*t + np.pi/2))  

qpsk_signal = (I*carrier_cos) - (Q*carrier)

print("QPSK Signal: ", qpsk_signal)

# Demodulation

bpsk_demod = bpsk_signal * carrier          # Multiplying by carrier(sin) makes value positive
                                            # and isolates signal value

bits_de_bpsk = np.sign(bpsk_demod)

print("Dedmodulated BPSK: ", bits_de_bpsk)

bits_de_bpsk_sections = len(signal) / samples_per_bit
bits_de_bpsk_final = np.array_split(bits_de_bpsk, (len(signal) / samples_per_bit))

bpsk_final = np.zeros(len(bits_de_bpsk_final), dtype=int)

counter = 0

for bunch in bits_de_bpsk_final:
    total = 0
    amt = 0
    for single_bit in bunch:
        total += single_bit
        amt += 1
    avg = int(((total / amt) + 1) / 2)
    bpsk_final[counter] = avg
    counter += 1


#print("Demodulated BPSK Signal: ", bits_de_bpsk_final)

# Verification

print("FINAL DEMODULATED BPSK: ", bpsk_final)

print("FINAL CHECK: ", bpsk_final == bits)