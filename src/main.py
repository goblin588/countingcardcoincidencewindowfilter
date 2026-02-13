from .detector import Logic16

# Settings 
DELAY_1 = 10
DELAY_2 = 20
DELAY_3 = 30
DELAY_4 = 40

TRIGG_CH = 8
DET_CH1 = 1
DET_CH2 = 2
DET_CH3 = 3

DET_CHS = [DET_CH1, DET_CH2, DET_CH3]

SINGLE_DET_CHS = [TRIGG_CH, *DET_CHS]
COINCIDENCE_CHS = [[TRIGG_CH, ch] for ch in DET_CHS] 
COINCIDENCE_WINDOW = 2.0

def main():
    print("Hello from countingcardcoincidencewindowfilter!")

    with Logic16(coincidence_window=COINCIDENCE_WINDOW, logic_mode=True) as logic:
        logic.set_input_threshold(default_threshold=0.5)

        logic.set_channels(
            singles=SINGLE_DET_CHANNELS,
            coincidences=COINCIDENCE_CHS
        )

        logic.set_delays({
            1: DELAY_1,
            2: DELAY_2,
            3: DELAY_3,
            8: 0,
        })

        logic.set_coincidence_window(COINCIDENCE_WINDOW)  # ns

        c_counts, s_counts, integration_time = logic.read_counts_integrated(
            pos_coincidence=COINCIDENCE_CHS,
            pos_singles=SINGLE_DET_CHS
        )  


if __name__ == "__main__":
    # Perform 3 integration window readouts
    for i in range(len(3)):
        main()

