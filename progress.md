## TODO ITEMS
1. User input of bits; turn into library
2. Noise simulating moving through air waves
3. Filtering
4. Visual graph of waves, noise, filtering


## NEXT ITEM
1. Finish base code
2. Add hardware-level
3. Audio signal capture


Real hardware acquisition — you originally asked about sound card / DAQ signal capture. If you actually build the sound-card-in pipeline and feed a real generated square wave (from a function generator or microcontroller) through it, rather than only simulating everything in NumPy, that's a meaningfully different and more impressive claim: "captured and processed a live analog signal" vs. "simulated a signal in an array." This is genuinely the single biggest lever available to you here.

A real BER-vs-SNR curve with proper theoretical comparison — plotting your simulated BER against the theoretical BPSK/QPSK BER curve (there are closed-form equations for this, Q-function based) shows you understand the underlying math, not just the mechanics. This is a step above what most student projects do.

Carrier recovery / Costas loop — you flagged this as "harder mode" earlier and correctly skipped it for a first pass. If you come back and actually implement even a basic phase-locked loop or Costas loop, that's genuinely a differentiating, non-trivial DSP skill — most intern-level projects don't attempt this.

Something applied/novel on top — e.g., simulate a specific real protocol's parameters (Wi-Fi, LoRa, a satellite comms standard's known scheme), or add a real channel impairment beyond AWGN (multipath fading, frequency offset, timing jitter) — these show you're thinking about real-world RF conditions, not just the clean-textbook case.