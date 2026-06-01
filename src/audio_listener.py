import sounddevice as sd
import numpy as np
import time
import threading
import datetime

# Configuration
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # ~23ms per chunk

# DSP Configuration
PEAK_THRESHOLD = 15000  # High amplitude threshold to ignore typing and vocals
QUIET_THRESHOLD = 3000  # Maximum amplitude considered "quiet"
COOLDOWN_SEC = 0.75  # 750ms cooldown

# Pre-computed FIR filter kernel for a 3000 Hz High-Pass Filter (fs=44100, 31 taps)
FIR_KERNEL = np.array([
    -2.16971556e-04,  6.03168083e-04,  1.94720157e-03,  4.06910641e-03,
     6.71514934e-03,  8.93073054e-03,  9.11629509e-03,  5.36521605e-03,
    -3.98346666e-03, -1.97315350e-02, -4.13434897e-02, -6.67791202e-02,
    -9.27306323e-02, -1.15239700e-01, -1.30551127e-01,  8.63470186e-01,
    -1.30551127e-01, -1.15239700e-01, -9.27306323e-02, -6.67791202e-02,
    -4.13434897e-02, -1.97315350e-02, -3.98346666e-03,  5.36521605e-03,
     9.11629509e-03,  8.93073054e-03,  6.71514934e-03,  4.06910641e-03,
     1.94720157e-03,  6.03168083e-04, -2.16971556e-04
], dtype=np.float32)

class AudioListener:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.stream = None
        self.last_trigger_time = 0
        
        history_size = 5
        self.peak_history = [0] * history_size
        
        # Keep track of the last len(FIR_KERNEL)-1 samples from the previous chunk
        # so we can use np.convolve with mode='valid' seamlessly across chunks.
        self.overlap_buffer = np.zeros(len(FIR_KERNEL) - 1, dtype=np.float32)

    def log(self, msg):
        try:
            with open("smash_debug.log", "a") as f:
                f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")
        except:
            pass

    def start(self):
        if not self.running:
            self.running = True
            self.log("Starting audio listener...")
            
            def audio_callback(indata, frames, time_info, status):
                if status:
                    self.log(f"Stream status: {status}")
                
                audio_data = indata[:, 0].astype(np.float32)

                # Prepend the overlap buffer from the previous chunk
                padded_data = np.concatenate((self.overlap_buffer, audio_data))
                
                # Apply High-Pass Filter using fast numpy convolution
                filtered_data = np.convolve(padded_data, FIR_KERNEL, mode='valid')
                
                # Update overlap buffer with the end of the current chunk
                self.overlap_buffer = audio_data[-(len(FIR_KERNEL) - 1):]
                
                current_peak = np.max(np.abs(filtered_data))
                
                self.peak_history.pop(0)
                self.peak_history.append(current_peak)

                now = time.time()
                if now - self.last_trigger_time < COOLDOWN_SEC:
                    return

                is_clipping = current_peak > PEAK_THRESHOLD
                was_quiet = all(p < QUIET_THRESHOLD for p in self.peak_history[:-2])

                if is_clipping and was_quiet:
                    self.last_trigger_time = now
                    self.log(f"TRIGGERED! Peak: {current_peak:.2f}")
                    threading.Thread(target=self.callback, daemon=True).start()

            try:
                self.stream = sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', blocksize=CHUNK, callback=audio_callback)
                self.stream.start()
                self.log("Stream started successfully.")
            except Exception as e:
                self.log(f"Failed to start stream: {e}")

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.log("Audio listener stopped.")

    def cleanup(self):
        self.stop()
