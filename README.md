# messin_with_tles


** WORK IN PROGRESS. THis document is intended for internal use only. **

## TODOS:
- ~~brute force all tles in obs window~~

Buildout script functionality:
- getopt
- config file reading and error messages
- requirements.txt or setup.py

Cleanup:
- Extend ephem.observer to allow for other params e.i. beam-width and buffer zone (sidelobes??)
- Write a better readme
- Proper docstrings

Speedup:
- Peak-trough-incline-decline algorithm (CAUTION: edge cases where orbit is longer than obs window) 
- Look into caching 
- Think about multipe targets in single run (cost effective??)


## Progress:
3/4/2020: Running `$ time pos_calc.py` yields `user	0m12.801s`. Much faster than previous iteration, simply checking the `ephem.Body.next_rising` field

