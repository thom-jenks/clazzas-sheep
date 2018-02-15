#!/usr/bin/env python2
import pandas
import matplotlib.pyplot as plt
import numpy as np
import os

pos_confidence = 19
collar_id = 11
y_pos = 13
pos_confidence_thres = 0.8

def make_dir(infile):
    dirname = infile[:-4]
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname

def plot_data(collar, data, indir):
    print("Plotting histogram for collar {}".format(collar))
    fig, ax = plt.subplots()
    ax.set_title("Histogram of y-position for collar {}".format(collar))
    ax.set_ylabel("Frequency")
    ax.set_xlabel("y position")
    n, bins, patches = plt.hist(data[y_pos], edgecolor='black', normed=True)
    rows = []

    f = open("{}/{}_histogram.csv".format(indir, collar), "w")
    f.write("lower_bound,upper_bound,frequency,proportion,percentage\n")
    for i in range(len(n)):
        prop = (bins[i + 1] - bins[i])*n[i]
        f.write("{},{},{},{},{}\n".format(bins[i], bins[i + 1], n[i], prop, prop*100))
        rows.append((bins[i], bins[i + 1], n[i]))
    
    fig.savefig("{}/{}.pdf".format(indir, collar))
    fig.clear()

def write_stats(collar, data, indir):
    print("Writing statistics of collar")
    mean = data[y_pos].mean()
    std = data[y_pos].std()
    print("{} samples: ".format(data[y_pos].count()))

    f = open("{}/{}.stats".format(indir, collar), "w")
    f.write("mean: {}\n".format(mean))
    f.write("std_deviation: {}\n".format(std))

def analyze_sheep(collar, df, infile):
    data = df[df[collar_id] == collar]

    dirname = make_dir(infile)
    print("Output dir: {}".format(dirname))
    
    plot_data(collar, data, dirname)
    write_stats(collar, data, dirname)
    
    
def main(infile):
    print("Reading data from {}".format(infile))
    # use_cols refers to y_position and position_confidence.
    df = pandas.read_csv(infile, header=None, usecols=[y_pos, collar_id, pos_confidence])
    df = df[df[pos_confidence] > pos_confidence_thres]
    for collar in df[collar_id].unique():
        analyze_sheep(collar, df, infile)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: {} <csv_file>".format(sys.argv[0]))
        exit(1)
    main(sys.argv[1])
