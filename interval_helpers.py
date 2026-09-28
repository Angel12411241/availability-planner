from interval import Interval
from collections import deque
def normalize_intervals(intervals: list[Interval]) -> list[Interval]:
    """
    First the intervals are sorted by "start", than are normalized:
    If we have intervals [10,100), [80,150), than we have [10,150)

    Time complexity: O(nlogn) + O(n) ~= O(nlogn), where n is the number of intervals in "intervals"
    """ 
    if len(intervals) == 0:
        return []
    
    intervals = sorted(intervals, key=lambda x: (x.start, x.end))
    res = [intervals[0]]
    for i, interval in enumerate(intervals):
        if interval.start >= interval.end:
            raise ValueError("Start of interval must be less than end of interval!")

        if i == 0: continue
        
        if res[-1].end > interval.start: # Use > as the "end" is exclusive
            res[-1].end = max(res[-1].end, interval.end)
        
        else:
            res.append(interval)

    return res

def intersect_intervals(interval1: list[Interval], interval2: list[Interval]) -> list[Interval]:
    """
    Time complexity: O(n), where n is the total number of intervals, both in interval1 and interval2
    Space complexity: O(n), the result itself
    """
    i = 0
    j = 0
    res = []
    while i < len(interval1) and j < len(interval2):
        start = max(interval1[i].start, interval2[j].start)
        end = min(interval1[i].end, interval2[j].end) 

        if start < end:
            res.append(Interval(start, end))

        if interval1[i].end < interval2[j].end:
            i+=1
        else:
            j+=1

    return res

def remove_intervals_outside_of_horizon(horizon: list[Interval], intervals: list[Interval]) -> list[Interval]:
    """
    Time complexity: O(n) + O(n) + O(n) ~= O(n), where n is the number of intervals in "intervals"
    Space complexity: O(n)(because of the deque)

    We need the deque as if we have 100k elements pop(0) is O(n) operation, thus the time complexity will result in O(n^2)
    """
    i = 0
    j = len(intervals) - 1
    intervals = deque(intervals)

    while i <= j:
    
        if intervals[j].start > horizon.end:
            intervals.pop()
            j-=1
        elif intervals[j].end > horizon.end:
            intervals[j].end = horizon.end

        if intervals[i].end < horizon.start:
            intervals.popleft()
            i+=1
        elif intervals[i].start < horizon.start:
            intervals[i].start = horizon.start
        
        i+=1
        j-=1
        
    return list(intervals)