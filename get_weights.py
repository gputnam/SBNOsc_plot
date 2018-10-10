import ROOT
import os
import sys
from array import array
import argparse
import math

def main(args):
    # get input file -- should be output from sbn -m SBNOsc_NuMuSelection
    input_file = ROOT.TFile(args.input)
    input_tree = input_file.Get("sbnana")
    for entry in input_tree:
        # get the weights
        weights = entry.events.truth[0].weights
        for key in weights:
            print key[0]
        break
if __name__ == "__main__":
    buildpath = os.environ["SBN_LIB_DIR"]
    if not buildpath:
        print "ERROR: SBNDDAQ_ANALYSIS_BUILD_PATH not set"
        sys.exit() 
    ROOT.gROOT.ProcessLine(".L " + buildpath + "/libsbnanalysis_Event.so") 
    ROOT.gROOT.ProcessLine(".L " + buildpath + "/libsbnanalysis_SBNOsc_classes.so") 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    main(parser.parse_args())
