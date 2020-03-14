# find_sat_flybys


** WORK IN PROGRESS. THis document is intended for internal use only. **

## TODOS:
- ~~brute force all tles in obs window~~

Buildout script functionality:
- ~~getopt~~
- ~~convert engligh times to ms (12m -> 720000)~~
- ~~config file reading~~ and error messages 
- requirements.txt or setup.py
- Install
- use cache

Cleanup:
- ~~Extend ephem.observer to allow for other params~~ 
- Figure out hat to do w/ beam-width and buffer zone (sidelobes??)
- Write a better readme
- ~~rename repo~~
- ~~Proper docstrings~~
- Take care of `#TODO`s
- Proper docstrings for PTID


Speedup:
- ~~Peak-trough-incline-decline algorithm prelim catagorization~~
- ~~Peak-trough-incline-decline algorithm recursive part~~
- ~~PTID algorithm edge cases where obs window is longer than orbit~~
- ~~Look into caching~~
- ~~Think about multipe targets in single run (cost effective??)~~
- Write hashmap wrapper for targettimeseries
- Compare ^^ to iterative list[hasmap] creation
- Integrate wrapper for targettimeseries

Caching tles:
- Find way to get old tles
- Write lru cache data to cache metadata file (reads, writes, evict) 
- Check cache -> in cache ? yield file : query db to file, yield file
- Cache settings file 

Testing
- hookup travis
- Write main test for pos calc


## Progress:
3/4/2020: 
- Running `$ time pos_calc.py` yields `user	0m12.801s`. Much faster than previous iteration, simply checking the `ephem.Body.next_rising` field
- Arg parser workin like a dream

3/9/2020: 
- distance function working after much head scratching

3/11:
- Rough implementation of ptid. **20x speedup increase!** `time` yeilds `user 0m0.624s`
