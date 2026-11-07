import numpy as np

fs = 100                                                # sampling rate []
fc = 40                                     # carrier frequency (Hz) 
# fc must be less than fs/2 (NyQuist)
bit_rate = 10
samples_per_bit = int(fs / bit_rate)
samples_per_symbol = 2 * samples_per_bit    # for QPSK

noise_std = 0.3                             # noise standard deviation

#bits = np.array([0, 1, 1, 0])               # message
bits = np.random.randint(0, 2, 20000)


#-----------------BPSK-----------------------------
symbols = (bits*2) - 1                                              # 0 => -1; 1 => 1

signal = np.repeat(symbols, samples_per_bit)                        # symbols // signal

t = np.arange(len(signal)) / fs
# evenly split array of total duration

# Transmitter
carrier = np.sin(2 * np.pi * fc * t)
# bit 0 - pi degree modulation phase | same as multiply by -1
# 1 - 0 degree modulation phase

bpsk_signal = carrier * signal                                      # bit 0 - pi degree modulation phase, bit 1 = 0 phase

# Channel
noise = np.random.normal(0, noise_std, len(bpsk_signal))


# Receiver
received_signal = bpsk_signal + noise

t_rx = np.arange(len(received_signal)) / fs
receiver_carrier = np.sin(2 * np.pi * fc * t_rx)

mixed = received_signal * receiver_carrier * 2                      # multiply by 2 since carrier not always at 1

bit_values = mixed.reshape(-1, samples_per_bit).mean(axis=1)

bpsk_final = (bit_values > 0).astype(int)                           # round up or down

print("BPSK, Matches input bits: ", np.array_equal(bpsk_final, bits))
print("BPSK, BER: ", np.mean(bpsk_final != bits))


#-------------------QPSK----------------------------        --> ORTHOGONAL
I_bits = bits[0::2]
Q_bits = bits[1::2]

I_symbols = I_bits*2 - 1                                            # 0 --> -1
Q_symbols = Q_bits*2 - 1                                            # 1 -->  1

I_stream = np.repeat(I_symbols, samples_per_symbol)
Q_stream = np.repeat(Q_symbols, samples_per_symbol)

# Transmitter
t = np.arange(len(I_stream)) / fs                                   # redefine t
qpsk_signal = (I_stream * np.cos(2 * np.pi * fc * t)) - (Q_stream * np.sin(2 * np.pi * fc * t))

# Channel
noise = np.random.normal(0, noise_std, len(qpsk_signal))

# Receiver
received_qpsk_signal = qpsk_signal + noise

t_rx = np.arange(len(received_qpsk_signal)) / fs
qpsk_cos_carrier = np.cos(2 * np.pi * fc * t_rx)
qpsk_sin_carrier = np.sin(2 * np.pi * fc * t_rx)

I_mixed = received_qpsk_signal * qpsk_cos_carrier * 2
Q_mixed = received_qpsk_signal * qpsk_sin_carrier * -2

I_values = I_mixed.reshape(-1, samples_per_symbol).mean(axis=1)
Q_values = Q_mixed.reshape(-1, samples_per_symbol).mean(axis=1)

qpsk_bits = np.empty(len(bits), dtype=int)
qpsk_bits[0::2] = (I_values > 0)
qpsk_bits[1::2] = (Q_values > 0)

print("QPSK, Matches input bits:", np.array_equal(qpsk_bits, bits))
print("QPSK, BER:", np.mean(qpsk_bits != bits))


#--------------------------VERIFICATION-------------------------
# using functions so test cases can be ran with different noise levels & with intentionally wrong receiver carrier phase

def bpsk_link(msg, noise_std = 0.0, rx_phase = 0.0):
    tx_t = np.arange(len(msg) * samples_per_bit) / fs
    tx = np.repeat(msg * 2 - 1, samples_per_bit) * np.sin(2 * np.pi * fc * tx_t)
    rx = tx + np.random.normal(0, noise_std, len(tx))
    tr = np.arange(len(rx)) / fs
    v = (rx * np.sin(2 * np.pi * fc * tr + rx_phase) * 2).reshape(-1, samples_per_bit).mean(axis=1)
    return (v > 0).astype(int)


def qpsk_link(msg, noise_std = 0.0, rx_phase = 0.0):
    I = np.repeat(msg[0::2] * 2 - 1, samples_per_symbol)
    Q = np.repeat(msg[1::2] * 2 - 1, samples_per_symbol)

    tx_t = np.arange(len(I)) / fs
    tx = I * np.cos(2 * np.pi * fc * tx_t) - Q * np.sin(2 * np.pi * fc * tx_t)
    rx = tx + np.random.normal(0, noise_std, len(tx))
    tr = np.arange(len(rx)) / fs
    iv = (rx * np.cos(2 * np.pi * fc * tr + rx_phase) * 2).reshape(-1, samples_per_symbol).mean(axis = 1)
    qv = (rx * np.sin(2 * np.pi * fc * tr + rx_phase) * -2).reshape(-1, samples_per_symbol).mean(axis = 1)

    out = np.empty(len(msg), dtype=int)
    out[0::2] = iv > 0
    out[1::2] = qv > 0

    return out

def ber(link, **kw):
    return np.mean(link(bits, **kw) != bits)


schemes = {"BPSK": bpsk_link, "QPSK": qpsk_link}
levels = [0.5, 1.0, 1.5, 2.0, 3.0]

# Cases

# 1. BER vs noise

print("noise_std    BPSK BER    QPSK BER")
sweep = {name: [ber(link, noise_std=s) for s in levels] for name, link in schemes.items()}
for i, s in enumerate(levels):
    print(f"{s:<11}  {sweep['BPSK'][i]:<10.4f}  {sweep['QPSK'][i]:.4f}")
print()

# 2. Wrong receiver carrier phase w/ a bit of noise so decision not left to rounding

print("Wrong receiver carrier phase (noise_std = 0.3)")
print("phase      BPSK BER    QPSK BER")
phase_ber = {}
for label, ph in [("0 deg", 0.0), ("90 deg", np.pi / 2), ("180 deg", np.pi)]:
    phase_ber[label] = {name: ber(link, noise_std=0.3, rx_phase=ph) for name, link in schemes.items()}
    print(f"{label:<9}  {phase_ber[label]['BPSK']:<10.3f}  {phase_ber[label]['QPSK']:.3f}")
print()

# 3) Pass / fail summary
for name, link in schemes.items():
    clean_ok = ber(link, noise_std=0.0) == 0
    low_ok = ber(link, noise_std=0.3) == 0
    rises_ok = all(b2 >= b1 for b1, b2 in zip(sweep[name], sweep[name][1:]))
    phase_ok = (0.4 < phase_ber["90 deg"][name] < 0.6) and (phase_ber["180 deg"][name] > 0.95)
    print(f"{name}: noise-free exact recovery {'PASS' if clean_ok else 'FAIL'} | "
          f"zero errors at 0.3 {'PASS' if low_ok else 'FAIL'} | "
          f"BER rises with noise {'PASS' if rises_ok else 'FAIL'} | "
          f"wrong phase breaks demod {'PASS' if phase_ok else 'FAIL'}")