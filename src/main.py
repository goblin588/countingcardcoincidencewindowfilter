# from detector import Logic16
# from settings import SINGLE_DET_CHS, COINCIDENCE_WINDOW, COINCIDENCE_CHS, DELAYS

# def main():
#     print("Hello from countingcardcoincidencewindowfilter!")

#     with Logic16(coincidence_window=COINCIDENCE_WINDOW, logic_mode=True) as logic:
#         logic.set_input_threshold(default_threshold=0.5)

#         logic.set_channels(
#             singles=SINGLE_DET_CHS,
#             coincidences=COINCIDENCE_CHS
#         )

#         # logic.set_delays({
#         #     1: DELAYS[1],
#         #     2: DELAYS[2],
#         #     3: DELAYS[3],
#         #     8: DELAYS[0],
#         # })

#         # logic.set_coincidence_window(COINCIDENCE_WINDOW)  # ns

#         # Perform 3 integration window readouts
#         samples = 50
#         for i in range(0, samples):

#             c_counts, s_counts, integration_time = logic.read_counts_integrated(
#                 pos_coincidence=COINCIDENCE_CHS,
#                 pos_singles=SINGLE_DET_CHS
#             )  

#             print(f'c counts: c_counts, s counts: {s_counts}')

# if __name__ == "__main__":
#     main()



import time
import numpy as np
from detector import Logic16
from settings import SINGLE_DET_CHS  # e.g., [1]

SINGLE_DET_CHS = [8]
COINCIDENCE_CHS = [[]]  # Example: channel 1 in coincidence with channels 2, 3, and 4  

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
    live_single_channel_stream(duration=20.0)  

