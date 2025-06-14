import os
import subprocess
import time

# Parameters
start_freq = 24_000_000       # 24 MHz
end_freq = 1_500_000_000      # 1.5 GHz
step_freq = 2_400_000         # 2.4 MHz (max sample rate of RTL-SDR)
sample_rate = 2_400_000       # 2.4 MSPS
duration_sec = 0.1            # 100 ms
samples = int(sample_rate * duration_sec)
gain = 20                     # Adjust as needed
output_dir = "iq_data"

os.makedirs(output_dir, exist_ok=True)

for freq in range(start_freq, end_freq + 1, step_freq):
    out_file = os.path.join(output_dir, f"iq_{freq//1_000_000}MHz.iq")
    print(f"[+] Capturing {freq / 1_000_000:.3f} MHz -> {out_file}")

    cmd = [
        "rtl_sdr",
        "-f", str(freq),
        "-s", str(sample_rate),
        "-n", str(samples),
        "-g", str(gain),
        out_file
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] rtl_sdr failed at {freq} Hz: {e}")
    
    time.sleep(0.1)  # Optional delay between captures

print("[✓] Sweep complete.")
