# indicators/logic3.py

def volume_oscillator(volume_series, short_window=3, long_window=10):
    """
    Basic Volume Oscillator stub.
    VO = SMA(volume, short_window) - SMA(volume, long_window)
    """
    if len(volume_series) < long_window:
        return None

    short_avg = sum(volume_series[-short_window:]) / short_window
    long_avg = sum(volume_series[-long_window:]) / long_window
    return short_avg - long_avg
