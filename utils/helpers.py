# utils/helpers.py

from datetime import datetime

def align_to_bar_boundary(dt: datetime, bar_length=30):
    """
    Anchors dt to the most recent bar boundary in multiples of 'bar_length' seconds.
    E.g. for bar_length=30, anchor to :00 or :30 of each minute.
    """
    second_of_minute = dt.second
    remainder = second_of_minute % bar_length
    anchored_second = second_of_minute - remainder
    return dt.replace(second=anchored_second, microsecond=0)
