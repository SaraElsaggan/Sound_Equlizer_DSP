import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the normal ECG signal from CSV
normal_ecg_df = pd.read_csv('normal_ecg.csv', header=None)
abnormal_ecg_df = pd.read_csv('abnormal_ecg.csv', header=None)
bidmc_01_Signals_df = pd.read_csv('bidmc_01_Signals.csv', header=None)

# Extract time and amplitude columns by index
time = normal_ecg_df[0]
normal_signal = normal_ecg_df[1].to_numpy()  # Convert to NumPy array

# Function to add artificial arrhythmia
def add_arrhythmia(ecg_signal, arrhythmia_start, arrhythmia_duration, arrhythmia_amplitude):
    arrhythmia = arrhythmia_amplitude * np.sin(
        np.linspace(0, 2 * np.pi, int(arrhythmia_duration * 1000))
    )

    # Ensure arrhythmia signal is the same length as the portion to be replaced
    arrhythmia = np.resize(arrhythmia, len(ecg_signal[arrhythmia_start:arrhythmia_start + len(arrhythmia)]))

    # Convert the slice to a NumPy array before addition
    ecg_signal[arrhythmia_start:arrhythmia_start + len(arrhythmia)] = (
        ecg_signal[arrhythmia_start:arrhythmia_start + len(arrhythmia)] + arrhythmia
    )

# Example: Add arrhythmia starting at 5 seconds, lasting for 2 seconds, and with an amplitude of 0.5
add_arrhythmia(normal_signal, int(7 * 1000), int(9 * 1000), 20)

# Create a new DataFrame with the modified ECG signal
modified_ecg_df = pd.DataFrame({'Time': time, 'Amplitude': normal_signal})

# Save the modified signal to a new CSV file
modified_ecg_df.to_csv('file_ecg_1.csv', index=False)

plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot( normal_ecg_df[0], normal_ecg_df[1])
plt.title('Original ECG Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Plot the modified signal
plt.subplot(3, 1, 2)
plt.plot(abnormal_ecg_df[0],abnormal_ecg_df[1])
# plt.plot(time, modified_ecg_df["Amplitude"])
plt.title('Modified ECG Signal with Arrhythmia')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# # Plot the difference
plt.subplot(3, 1, 3)
plt.plot( bidmc_01_Signals_df[0], bidmc_01_Signals_df[1])
# plt.plot(time, modified_ecg_df["Amplitude"] - normal_ecg_df[1])
plt.title('Difference between Original and Modified Signals')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')


plt.tight_layout()
plt.show() 