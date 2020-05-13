# find_sat_flybys

find_sat_flybys is a program that will calculate the positions of active satellites for a given observation and report if any satellites enter the beam (or come close).

The main improvement is the PTID (peak, trough, incline, decline) algorithm which analyzes the slope of the (distance from target to beam) function to classify the function as representing a peak, trough, incline or decline over the specified observation window. If a trough is found, I can basically do a binary search to find a local extrema and there will only be one (see limitations)

The PTID algorithm takes the calculation of an individual satellite from O(t) to O(lg(t)) where t is the length of the observation in milliseconds.

### Limitations 

- Observations of one target have a max length of 42.5 minutes. This is because the fastest LEO satellites have an orbital period of 85 minutes. THis makes the algorithm simpler but it's possible to add this functionality later

- Right now, the program is only able to check observation times at most a week from the time the script is run. This means it can't be used to check observations more than a week old. Likewise, it can't be used to check observation plans more than a week in the future. This is because, in it's current version, the program is using the celestrak database which just posts currently active, up-to-date TLEs. Spacetrak offers archival queries but they don't have a way to query only the actively transmitting TLEs. This means you would have to query 40 million TLEs and filter them. I'm talking so one of their site admins so hopefully we can find a solution. 


## Note
Because the potential user base is small for this project, I didn't do a ton of work on the UI. This was intentional, if you think I should make this a python module or really dial in the CLI or even make a REST api, let me know. Maybe a checker that takes in hdf5/fil files?

## Install

Clone this repo and cd into the base directory then run:
```
pip3 install -r requirements.txt
```

### Configure

You must create a config file. The example is `config.yaml` with will show you what values you need. [This link](https://github.com/UCBerkeleySETI/blimpy/blob/master/blimpy/ephemeris/observatory_info.csv) might help.

### Running

The following arguments are required:\
	-ra/--right_ascension (radians, float), coordinated of the observation target\
	-dec/--declination (radians, float), "\
	-d/--duration, observation duration abbreviated e.g. 12m, 30s\
	-s/--start_utc, start of the observation, defaults to now\
The folowing argumets are optional:\
	-f/--config_filename, defaults to config.yaml\
	-v, verbosity\
	-r/--radius will override the beam_width_arcmin setting from config.yaml\

An example command looks like this:
```
python3 find_flybys.py -f config.yaml -ra 0.40 -dec 0.40 -d 35m -v -r 2.0 -s 1589390462
```
The argparser is pretty thorough so if you mess up the arguments, it should tell you how to fix it.

For example, I opened up the beam to 10 arcmins and the beam_proximity_buffer to 20 arcmins and got the following:
```
$ python3 find_flybys.py -f config.yaml -ra 0.40 -dec 0.40 -d 35m -v -r 200 -s 1589390462
Sats in beams:  6
	 YAOGAN 19    closest distance: 5.95796 arcmins
	 STARLINK-26    closest distance: 2.06805 arcmins
	 2019-032A    closest distance: 1.95543 arcmins
	 2019-032C    closest distance: 6.06539 arcmins
	 2019-032D    closest distance: 6.09648 arcmins
	 2019-032E    closest distance: 5.91181 arcmins
Sats in proximity:  3
	 TIROS N    closest distance: 13.41159 arcmins
	 FENGYUN 3C    closest distance: 17.86240 arcmins
	 CE-SAT-I    closest distance: 16.60994 arcmins
```


## TODOS:
** WORK IN PROGRESS. THis section of the readme document is intended for internal use only. **

- ~~brute force all tles in obs window~~

Build out script functionality:
- ~~getopt~~
- ~~convert engligh times to ms (12m -> 720000)~~
- ~~config file reading~~ and error messages 
- ~~requirements.txt or setup.py~~
- ~~Install~~
- use cache

Cleanup:
- ~~Extend ephem.observer to allow for other params~~ 
- ~~Figure out hat to do w/ beam-width and buffer zone (sidelobes??)~~ Not caring about this for now bc it's plenty fast so I dont need to optimize
- ~~Write a better readme~~
- ~~rename repo~~
- ~~Proper docstrings~~
- ~~Take care of `#TODO`s~~
- ~~Proper docstrings for PTID~~


Speedup:
- ~~Peak-trough-incline-decline algorithm prelim categorization~~
- ~~Peak-trough-incline-decline algorithm recursive part~~
- ~~PTID algorithm edge cases where obs window is longer than orbit~~
- ~~Look into caching~~
- ~~Think about multipe targets in single run (cost effective??)~~
- ~~Write hashmap wrapper, targettimeseries~~
- ~~Compare ^^ to iterative list[hasmap] creation~~ Kicks ass
- ~~Integrate wrapper for targettimeseries~~

Caching tles:
- Find way to get old tles
- Write lru cache data to cache metadata file (reads, writes, evict) 
- Check cache -> in cache ? yield file : query db to file, yield file
- Cache settings file 

Testing
- hookup travis
- Write main test for:
	- poscalc
	- target_timeseries
	- observatory
	- ptid
	- parser

## Progress:
3/4/2020: 
- Running `$ time pos_calc.py` yields `user	0m12.801s`. Much faster than previous iteration, simply checking the `ephem.Body.next_rising` field
- Arg parser workin like a dream

3/9/2020: 
- distance function working after much head scratching

3/11:
- Rough implementation of ptid. **20x speedup increase!** `time` yeilds `user 0m0.624s`

3/14:
- Targettimeseries speeds up runtime to ```user	0m0.458s``` but much better on memory as samplerate increases
