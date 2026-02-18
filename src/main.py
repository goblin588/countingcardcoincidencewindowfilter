from detector import Logic16
from settings import SINGLE_DET_CHS, COINCIDENCE_WINDOW, COINCIDENCE_CHS, DELAYS
import time
import numpy as np

def stream_delayed_coincidence_counts():
    print("Streaming delayed coincidence counts...")

    # Initialize coincidences dictionary with zero counts for each pair
    coincidences = {tuple(pair): 0 for pair in COINCIDENCE_CHS}

    with Logic16(coincidence_window=COINCIDENCE_WINDOW, logic_mode=True) as logic:
        logic.set_input_threshold(default_threshold=0.5)
        # logic.set_channels(
        #     singles=SINGLE_DET_CHS,
        #     coincidences=COINCIDENCE_CHS
        # )

        logic.set_delays({
            1: DELAYS[0],  # Delay for channel 1
            2: DELAYS[1],  # Delay for channel 2
            3: DELAYS[2],  # Delay for channel 3
            4: DELAYS[3],  # Delay for channel 4
            5: DELAYS[4],  # Delay for channel 5 (if used)
            6: DELAYS[5],  # Delay for channel 6 (if used)
            7: DELAYS[6],  # Delay for channel 7 (if used
            8: DELAYS[7],  # Delay for channel 8 (if used)
        })

        samples = 20
        for i in range(samples):
            c_counts, s_counts, delta_t = logic.read_counts(
                pos_coincidence=COINCIDENCE_CHS,
                pos_singles=SINGLE_DET_CHS
            )  

            # Accumulate coincidence counts
            for idx, pair in enumerate(COINCIDENCE_CHS):
                coincidences[tuple(pair)] += c_counts[idx]

            # Optional: print live single counts
            for ch, count in zip(SINGLE_DET_CHS, s_counts):
                print(f"Channel {ch} counts: {count}")

            # Short delay between loops (optional)
            time.sleep(0.1)

    # Print accumulated coincidences at the end
    print("\n=== Total Coincidence Counts ===")
    for key, count in coincidences.items():
        print(f"Channels {key} coincidence counts: {count}")


def live_single_channel_stream(duration=10.0):
    """
    Streams counts from a single channel in near-real-time.
    """
    print("Starting live counts...")
    
    with Logic16(logic_mode=True, integration_window=10.0) as logic:
        # logic.set_input_threshold(default_threshold=0.5)
        # logic.set_coincidence_window(2)  # ns
        # logic._integration_window = 0.5  # seconds, for very short integration (antilatch safe)
        # logic.set_delays({
        #     1: 100,  # No delay for channel 1
        #     2: 24  # No delay for channel 2
        # })

        # logic.set_channels(singles=SINGLE_DET_CHS, coincidences=COINCIDENCE_CHS)
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            # Read counts quickly, with very short integration (antilatch safe)
            counts, _, delta_t = logic.read_counts(
                pos_coincidence=COINCIDENCE_CHS,
                pos_singles=SINGLE_DET_CHS,
            )
            
            # counts is numpy array, one value per channel
            print(f'pos_singles: {SINGLE_DET_CHS}, pos_coincidence: {COINCIDENCE_CHS}, counts: {counts}, delta_t: {delta_t:.6f} s')
            # print(f"Channel {SINGLE_DET_CHS[0]} counts: {counts[0]} | Δt: {delta_t:.6f} s | Freq: {counts[0]/delta_t:.2f} Hz")
            
            # Optional: very short sleep to avoid hammering CPU
            time.sleep(0.05)

if __name__ == "__main__":
    # live_single_channel_stream(duration=20.0)  
    stream_delayed_coincidence_counts()

