from interval_helpers import normalize_intervals
from interval import Interval

class ResourceCalendar:
    def __init__(self, working: list[Interval], busy: list[Interval]):
        #I can have getter for working and busy if i want to keep the exact contract of the provided dataclass
        self._working = normalize_intervals(working)
        self._busy = normalize_intervals(busy) 
        self.free_intervals = self._generate_free_intervals()


    def _generate_free_intervals(self):
        """
        It checks self._working and self._busy and based on them it generates the free intervals
        Time Complexity: O(n+m)
        "n" is the number of intervals in self._working 
        "m" is the number of intervals in self._busy
        """
        res = []  
        busy_idx = 0

        for working in self._working:
            current_start = working.start
            #This assumes that we do not have busy intervals that go beyond the working interval's end
            #meaning that there is no busy:(10,50) and working:(0,40)
            while busy_idx < len(self._busy) and self._busy[busy_idx].start < working.end:

                if self._busy[busy_idx].start > current_start:
                    res.append(Interval(current_start, self._busy[busy_idx].start))

                current_start = max(current_start, self._busy[busy_idx].end)

                if current_start >= working.end:
                    break

                busy_idx += 1

            if current_start < working.end:
                res.append(Interval(current_start, working.end))

        return res