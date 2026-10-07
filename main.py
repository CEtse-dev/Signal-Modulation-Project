import numpy as np

fs = 100                                  # sampling rate []
f = 10                                    # frequency of 'actual signal'
fc = 40                                   # carrier frequency (Hz) 
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
# evenly split array of total duration
# timestamps shifted slightly (1+e-3) so never exactly 0... code dependent on +1/-1

print("Time stamps: ", t, "\n")

# With 'noise'----------
# noise = np.random.normal(0, 0.1, len(signal))
# noisy_signal = signal + noise
#signal = noisy_signal                              #--> includes noise as needed

# filtering-------------
    # signal variable treated as symbols for bits

# BPSK Modulation
carrier = np.sin(2*np.pi*fc*t)
    # bit 0 - pi degree modulation phase | same as multiply by -1
    # 1 - 0 degree modulation phase

bpsk_signal = carrier * signal

print("BPSK Signal: ", bpsk_signal, "\n")

# Channel 

noise = np.random.normal(0, 0.3, len(bpsk_signal))

# Receiver

received_signal = bpsk_signal + noise;

t_receiver = np.arange(len(bpsk_signal)) / fs

receiver_carrier = np.sin(2*np.pi*fc*t_receiver)

mixed = received_signal * receiver_carrier * 2              # multiply by 2 since carrier not always at 1

bit_values = mixed.reshape(-1, samples_per_bit).mean(axis=1)

bpsk_final = (bit_values > 0).astype(int)

print("Dedmodulated BPSK bits: ", bpsk_final)

print("BPSK, Matches input bits:           ", np.array_equal(bpsk_final, bits))

#QPSK --> the same just orthogonal

I_bits = bits[0::2]
Q_bits = bits[1::2]

I_symbols = I_bits*2 - 1                        # 0 --> -1
Q_symbols = Q_bits*2 - 1                        # 1 -->  1

samples_per_symbol = 2 * samples_per_bit

I_stream = np.repeat(I_symbols, samples_per_symbol)
Q_stream = np.repeat(Q_symbols, samples_per_symbol)

t = np.arange(len(I_stream)) / fs                      # redefine t
qpsk_signal = (I_stream * np.cos(2 * np.pi * fc * t)) - (Q_stream * np.sin(2 * np.pi * fc * t))    # actually addition; just mathematical equivalent

noise = np.random.normal(0, 0.3, len(qpsk_signal))

received_qpsk_signal = qpsk_signal + noise

qpsk_cos_carrier = np.cos(2 * np.pi * fc * t)
qpsk_sin_carrier = np.sin(2 * np.pi * fc * t)

I_mixed = received_qpsk_signal * qpsk_cos_carrier * 2
Q_mixed = received_qpsk_signal * qpsk_sin_carrier * -2

I_values = I_mixed.reshape(-1, samples_per_symbol).mean(axis=1)
Q_values = Q_mixed.reshape(-1, samples_per_symbol).mean(axis=1)


qpsk_bits = np.empty(len(bits), dtype=int)
qpsk_bits[0::2] = (I_values > 0)
qpsk_bits[1::2] = (Q_values > 0)

print("Matches input bits:           ", np.array_equal(qpsk_bits, bits))

