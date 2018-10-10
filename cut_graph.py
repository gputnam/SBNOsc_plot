import ROOT
import os
import sys
from array import array
import argparse
import math

cuts = ["Initial", "Track", "FV", "Length", "Vertex-Match", "AV Only"]

def main(args):
    # get input file -- should be output from sbn -m SBNOsc_NuMuSelection
    input_file = ROOT.TFile(args.input)
    input_graph = input_file.Get("Graph")

    # print them if specified
    if args.print_data:
        for cut, i in zip(cuts, range(input_graph.GetN())):
            print cut, input_graph.GetY()[i]
            
    # plot them
    plot(args, input_graph)
        
def plot(args, input_graph):
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 250,100,700,500)
    input_graph.Draw()
    input_graph.SetTitle("")
    xax = input_graph.GetXaxis()
    i = 0
    while i < xax.GetXmax():
        bin_index = xax.FindBin(i)
        xax.SetBinLabel(bin_index, cuts[i])
        i += 1
    xax.LabelsOption("h")
    xax.SetLabelSize(0.075)
    canvas.Update()

    if args.wait:
        raw_input("Press Enter to continue...")

    if args.output is not None:
        canvas.SaveAs(args.output)

if __name__ == "__main__":
    buildpath = os.environ["SBN_LIB_DIR"]
    if not buildpath:
        print "ERROR: SBNDDAQ_ANALYSIS_BUILD_PATH not set"
        sys.exit() 
    ROOT.gROOT.ProcessLine(".L " + buildpath + "/libsbnanalysis_Event.so") 
    ROOT.gROOT.ProcessLine(".L " + buildpath + "/libsbnanalysis_SBNOsc_classes.so") 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-w", "--wait", action="store_true")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("-p", "--print_data", action="store_true")
    main(parser.parse_args())
