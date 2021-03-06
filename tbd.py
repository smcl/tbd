#!/usr/bin/python

# split this into separate files when > 100 lines ...

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import datetime
import dateutil.parser
import warnings

class TimeboxMethod():
   Seconds = 1
   Minutes = 2
   Hours = 3
   Days = 4

def stdin_from_pipe():
   return not os.isatty(sys.stdin.fileno())

# take input and return list of times
def read_input(datafile, separator):
   data = datafile.read()
  
   return [ dateutil.parser.parse(d) for d in data.split(separator) if d ]

# iterate over each time + box it (return dictionary)
def process_data(data, method):
   if method > TimeboxMethod.Seconds:
      data = [ d.replace(second=0) for d in data ]

   if method > TimeboxMethod.Minutes:
      data = [ d.replace(minute=0) for d in data ]

   if method > TimeboxMethod.Hours:
      data = [ d.replace(hour=0) for d in data ]

   output_data = {}

   for d in data:
      if d in output_data:
         output_data[d] += 1
      else:
         output_data[d] = 1
      
   return output_data

# take processed data and produce a graph
def plot_data(data, filename):
   x_data = data.keys()
   y_data = data.values()

   two_minutes = datetime.timedelta(0, 2)
   
   x_min = min(x_data) - two_minutes
   x_max = max(x_data) + two_minutes
   
   plt.xlim(x_min, x_max)
   
   plt.scatter(data.keys(), data.values())
   #plt.show()
   plt.savefig(filename)

def process_input_file(inputFile, inputFilename):
   outputFilename = inputFilename + ".png"
   raw_data = read_input(inputFile, "\n")

   data = process_data(raw_data, TimeboxMethod.Minutes) #temp

   print("saving to %s" % (outputFilename))
   plot_data(data, outputFilename)
   
# TODO: implement the following args using argparse:
# * --seconds, --minutes, --hours, --days
# * --show
# * --input-format=[csv,newline]

files = sys.argv[1:]

# suppress weird warnings in matplotlib
warnings.filterwarnings("ignore", module="matplotlib")

if stdin_from_pipe() and len(files) == 0:
   process_input_file(sys.stdin, "stdin")
else:
   for f in files:
      process_input_file(open(f), f)
