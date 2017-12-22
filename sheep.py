#!/usr/bin/env python2
import pandas
import matplotlib.pyplot as plt
import numpy as np
import os

pos_confidence = 19
collar_id = 11
y_pos = 13
pos_confidence_thres = 0.8

def plot_data(collar, data):
    print "Plotting histogram for collar {}".format(collar)
    f, ax = plt.subplots()
    ax.set_title("Histogram of y-position for collar {}".format(collar))
    ax.set_ylabel("Frequency")
    ax.set_xlabel("y position")
    plt.hist(data[y_pos], edgecolor='black', normed=True)
    f.savefig("{}.pdf".format(collar))
    f.clear()

def write_stats(collar, data):
    print "Writing statistics of collar"
    mean = data[y_pos].mean()
    std = data[y_pos].std()
    print "{} samples: ".format(data[y_pos].count())

    print "mean: {}".format(mean)
    print "std: {}".format(std)
    f = open("{}.stats".format(collar), "w")
    f.write("mean: {}\n".format(mean))
    f.write("std_deviation: {}\n".format(std))

def analyze_sheep(collar, df):
    data = df[df[collar_id] == collar]
    plot_data(collar, data)
    write_stats(collar, data)
    
    
def main(infile):
    print "Reading data from {}".format(infile)
    # use_cols refers to y_position and position_confidence.
    df = pandas.read_csv(infile, header=None, usecols=[y_pos, collar_id, pos_confidence])
    df = df[df[pos_confidence] > pos_confidence_thres]
    for collar in df[collar_id].unique():
        analyze_sheep(collar, df)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: {} <csv_file>".format(sys.argv[0])
        exit(1)
    main(sys.argv[1])
