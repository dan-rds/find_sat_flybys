'''-------------------------------------
tle_cache.py
tle_cache

    by Daniel Richards (github.com/dan-rds)
    Copyright © 2020 Daniel Richards. All rights reserved.
-------------------------------------- 
'''
import pickle
import os
class LRUCache(object):
	"""docstring for LRUCache"""
	def __init__(self, num_blocks, filenames):
		super(LRUCache, self).__init__()
		self.num_blocks = num_blocks
		self.filenames = filenames
	def dump_to_file(self):
		with open('cache_state.pkl', 'wb') as output:
			pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)


def file_constructor(cache_state_filename: str) -> LRUCache:
	if not os.path.isfile(cache_state_filename):
		print (cache_state_filename,": no such file found")
		exit(1)

	with open(cache_state_filename, 'rb') as state_file:
		return pickle.load(state_file)

# #with open('cache_state.pkl', 'wb') as output:
# c = LRUCache(90, ['f1', 'f2', 'f3'])
# c.dump_to_file()
# del c

   # pickle.dump(c, output, pickle.HIGHEST_PROTOCOL)

x = file_constructor("cache_state.pkl")
print(x.num_blocks, x.filenames)