from detector import Logic16
from settings import TRIGG_CH, DET_CHS, COINCIDENCE_WINDOW, DELAYS
import time


def stream_herald_and_signal(
    herald_ch: int = TRIGG_CH,
    signal_ch: int = DET_CHS[0],
    duration: float = 20.0,
    coincidence_window: float = COINCIDENCE_WINDOW,
    delays: list = DELAYS,
):
    """
    Streams singles counts from a herald channel and a single signal channel,
    plus their coincidence rate, in near-real-time.

    Args:
        herald_ch: Herald/trigger channel number.
        signal_ch: Signal detector channel number.
        duration: How long to stream for, in seconds.
        coincidence_window: Coincidence window in ns.
        delays: List of per-channel delays (index = channel - 1).
    """
    singles_chs = [herald_ch, signal_ch]
    coincidence_chs = [[herald_ch, signal_ch]]
    channel_delays = {i + 1: delays[i] for i in range(min(len(delays), 8))}

    print(f"Streaming herald (ch {herald_ch}) and signal (ch {signal_ch})...")

    with Logic16(coincidence_window=coincidence_window, logic_mode=True) as logic:
        logic.set_input_threshold(default_threshold=0.5)
        logic.set_coincidence_window(coincidence_window)
        logic.set_delays(channel_delays)

        start_time = time.time()
        while (time.time() - start_time) < duration:
            c_counts, s_counts, timecounter = logic.read_counts(
                pos_coincidence=coincidence_chs,
                pos_singles=singles_chs,
            )
            delta_t = timecounter * logic._resolution

            herald_rate = s_counts[0] / delta_t
            signal_rate = s_counts[1] / delta_t
            coinc_rate = c_counts[0] / delta_t

            print(
                f"Herald (ch {herald_ch}): {herald_rate:.1f} Hz | "
                f"Signal (ch {signal_ch}): {signal_rate:.1f} Hz | "
                f"Coincidences: {coinc_rate:.1f} Hz | "
                f"Δt: {delta_t:.4f} s"
            )

            time.sleep(0.05)


def scan_coincidences_over_delays(
    herald_ch: int = TRIGG_CH,
    signal_chs: list = DET_CHS,
    coincidence_window: float = COINCIDENCE_WINDOW,
    delays: list = DELAYS,
    integration_window: float = 0.5,
):
    """
    Accumulates coincidence counts between a herald channel and multiple signal
    channels, each with an independent delay set via the delays list.
    Uses read_counts_integrated for robust antilatch-safe accumulation.

    Args:
        herald_ch: Herald/trigger channel number.
        signal_chs: List of signal detector channel numbers.
        coincidence_window: Coincidence window in ns.
        delays: List of per-channel delays (index = channel - 1).
        integration_window: Integration time in seconds per measurement.
    """
    singles_chs = [herald_ch, *signal_chs]
    coincidence_chs = [[herald_ch, ch] for ch in signal_chs]
    channel_delays = {i + 1: delays[i] for i in range(min(len(delays), 8))}

    print(f"Scanning coincidences: herald ch {herald_ch} vs signal chs {signal_chs}")
    print(f"Delays (ns): { {ch: delays[ch - 1] for ch in signal_chs} }")

    with Logic16(
        coincidence_window=coincidence_window,
        logic_mode=True,
        integration_window=integration_window,
    ) as logic:
        logic.set_input_threshold(default_threshold=0.5)
        logic.set_coincidence_window(coincidence_window)
        logic.set_delays(channel_delays)

        c_counts, s_counts, total_time = logic.read_counts_integrated(
            pos_coincidence=coincidence_chs,
            pos_singles=singles_chs,
        )

        # Live singles summary
        print("\n=== Singles Rates ===")
        for ch, count in zip(singles_chs, s_counts):
            print(f"  Ch {ch}: {count / total_time:.1f} Hz")

        print("\n=== Coincidence Counts ===")
        for idx, pair in enumerate(coincidence_chs):
            count = c_counts[idx]
            rate = count / total_time if total_time > 0 else 0.0
            delay = delays[pair[1] - 1]
            print(
                f"  Ch {pair[0]} & Ch {pair[1]} "
                f"(delay {delay} ns): "
                f"{count} counts  |  {rate:.2f} Hz avg  |  "
                f"total time {total_time:.2f} s"
            )


if __name__ == "__main__":
    stream_herald_and_signal(duration=20.0)
    # scan_coincidences_over_delays()