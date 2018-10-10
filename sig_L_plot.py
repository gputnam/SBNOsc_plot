import ROOT
import os
import sys
from array import array
import argparse
import math

Ls = range(0,300,10)
Lnames = ["L" + str(x) for x in Ls]
file_suffixes = ["_" + x + ".root" for x in ["NoL"] + Lnames]

def main(args):
    # get input file -- should be output from sbn -m SBNOsc_NuMuSelection
    input_fnames = [args.input_base + x for x in file_suffixes]
    data = [get_data(ROOT.TFile(fname)) for fname in input_fnames]
    print_SN(data[1:])
    plot(args, data[1:])

def get_data(tfile):
    nsignal = 0
    nbkg = 0
    for event in tfile.Get("sbnana"):
        for interaction in event.numu_interaction:
            if abs(interaction.t_pdgid) == 13:
                nsignal += 1
            elif abs(interaction.t_pdgid) == 211:
                nbkg += 1
            else:
                assert(False)
    return (nsignal, nbkg)

def print_SN(data):
    for Lname, (S, B) in zip(Lnames, data):
        if B != 0:
            print "%s: %i %i %f" % (Lname, S, B, S / math.sqrt(B))
        else:
            print "%s: %i %i" % (Lname, S, B)
        
def plot(args, data):
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 250,100,700,500)
    ydata = []
    yerr = []
    for i,(name, length, (S, B)) in enumerate(zip(Lnames, Ls, data)):
        if B == 0:
            print "Warning: cut %s has zero background, skipping..." % name
            continue
        sig = S / math.sqrt(B)
        err_S2 = S / B
        err_B = S / (2 * B)
        err = math.sqrt(err_S2 + err_B * err_B) 
        ydata.append(sig)
        yerr.append(err)

    graph = ROOT.TGraphErrors(len(ydata))
    for i,(length, sig, err) in enumerate(zip(Ls, ydata, yerr)):
        graph.SetPoint(i, length, sig)
        if args.errors:
            graph.SetPointError(i, 0, err)
       
    graph.Draw()
    graph.SetTitle("Length Cut Optimization")
    graph.GetXaxis().SetTitle("Length Cut [cm]")
    graph.GetYaxis().SetTitle("\mathrm{Significance } (S/\sqrt{B})")

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
    parser.add_argument("-i", "--input_base", required=True)
    parser.add_argument("-w", "--wait", action="store_true")
    parser.add_argument("-o", "--output", default=None)
    parser.add_argument("-e", "--errors", action="store_true")
    main(parser.parse_args())
