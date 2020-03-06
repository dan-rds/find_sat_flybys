# messin_with_tles


** WORK IN PROGRESS. THis document is intended for internal use only. **

## TODOS:
- ~~brute force all tles in obs window~~

Buildout script functionality:
- ~~getopt~~
- ~~convert engligh times to ms (12m -> 720000)~~
- ~~config file reading~~ and error messages 
- requirements.txt or setup.py
- use update tle

Cleanup:
- ~~Extend ephem.observer to allow for other params~~ 
- Figure out hat to do w/ beam-width and buffer zone (sidelobes??)
- Write a better readme
- rename repo
- ~~Proper docstrings~~

Speedup:
- Peak-trough-incline-decline algorithm naive 
- PTID algorithm edge cases where obs window is longer than orbit
- Look into caching 
- Think about multipe targets in single run (cost effective??)

## Progress:
3/4/2020: 
- Running `$ time pos_calc.py` yields `user	0m12.801s`. Much faster than previous iteration, simply checking the `ephem.Body.next_rising` field
- Arg parser workin like a dream
