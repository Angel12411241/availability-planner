from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from interval_helpers import intersect_intervals, remove_intervals_outside_of_horizon
from interval import Interval
from resource_calendar import ResourceCalendar
"""
Notes: 
- The Specification mentions that the contract is kept and the lists contain Intervals, I can use Pydantic for dynamic argument checking if needed.
- I am checking only for the errors specified in the documentation otherwise there are a lot of things that need to be checked.
Which in production can and in my opinion should be done, even if there is a documentation specifiying more clearly the contract of the interfaces and
the interface is called by trusted sources. In my opinion the code should handle contracts wherever possible itself. 
As contracts defined only in documentation can often go unnoticed in real production enviroment. 
It is usually better to raise explicit errors in the code wherever possible.
"""   

@dataclass(frozen=True)
class AvailabilityResult:
    free_windows: list[Interval]
    earliest_slot: Interval | None


def find_availability(
    calendars: Mapping[str, ResourceCalendar],
    required_resources: Sequence[str],
    horizon: Interval,
    duration: int,
) -> AvailabilityResult:
    """
    Get free windows for first resource(machine)
    intersect where they match with the second resource, 
    than intersect the result of the first two with the 3rd one and so on
    the result are the free windows, than get the first one that is big enough
    if it is within the horizon. Remove all windows that are outside of the horizon

    Time complexity: O(m*n) + O(n) + O(n) ~= O(m*n)
    Space complexity: O(l)
    m: number of required resources
    n: number of intervals
    l: number of resulting free intervals(free_windows)

    Realistically this can be written and considered, assuming the m will be relatively small as complared to the number of intervals:
    Time complexity: O(n)
    Space complexity: O(n)
    """
    if len(required_resources) == 0:
        raise ValueError("No required resources were provided")
    if horizon.end <= horizon.start:
        raise ValueError("Horizon start must be lower than horizon end")
    if len(set(required_resources)) != len(required_resources): 
        raise ValueError("There is a repeating resource in required_resources")
    if required_resources[0] not in calendars:
        raise ValueError(f"{required_resources[0]} does not exist as a resource")

    free_windows = calendars[required_resources[0]].free_intervals

    for i in range(1, len(required_resources)):
        if required_resources[i] not in calendars:
            raise ValueError(f"{required_resources[i]} does not exist as a resource")
        
        free_windows = intersect_intervals(free_windows, calendars[required_resources[i]].free_intervals)

    free_windows = remove_intervals_outside_of_horizon(horizon, free_windows)
    earliest_slot = None
    for interval in free_windows:
        #Note: I would like to ask an interviewer if it should be >, but looking at the given inputs,results I chose >=
        if interval.end - interval.start >= duration:
            earliest_slot = Interval(interval.start, interval.start + duration)
            break

    return AvailabilityResult(free_windows=free_windows, earliest_slot=earliest_slot)

calendars = {
    "machine": ResourceCalendar(
        working=(Interval(0, 120),),
        busy=(Interval(50, 70), Interval(20, 40), Interval(35, 50)),
    ),
    "sensor": ResourceCalendar(
        working=(Interval(60, 130), Interval(10, 60)),
        busy=(Interval(90, 100),),
    ),
}

result = find_availability(
    calendars=calendars,
    required_resources=("machine", "sensor"),
    horizon=Interval(0, 120),
    duration=15,
)

print(result)