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
    sig_ratios = get_ratios(data[0], data[1:])
    ratio_errs = get_errors(data[0], data[1:])

    print_SN(data[1:])
    plot(args, sig_ratios, ratio_errs)

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

def get_ratios(baseline, data):
    n_sig_baseline = float(baseline[0])
    n_bkg_baseline = float(baseline[1])
    return [(d[0] / n_sig_baseline, d[1] / n_bkg_baseline) for d in data] 

def get_errors(baseline, data):
    n_sig_baseline = float(baseline[0])
    n_bkg_baseline = float(baseline[1])
    return [(math.sqrt(d[0]) / n_sig_baseline, math.sqrt(d[1]) / n_sig_baseline) for d in data] 

def print_SN(data):
    for Lname, (S, B) in zip(Lnames, data):
        if B != 0:
            print ("%s: %i %i %f" % (Lname, S, B, S / math.sqrt(B))),
        else:
            print ("%s: %i %i" % (Lname, S, B)),
        print "Contamination: %f" % (float(B) / S)
        
def plot(args, ratios, errs):
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 250,100,700,500)
    graph = ROOT.TGraphErrors(len(ratios))
    labels = []
    for i,(name, (S, B), (eS, eB)) in enumerate(zip(Lnames, ratios, errs)):
        graph.SetPoint(i, B, S)
        if args.errors:
            graph.SetPointError(i, eB, eS)
        if (i+1) % 2 == 0:
            continue
        labels.append(ROOT.TLatex(graph.GetX()[i], graph.GetY()[i], name))
       
    graph.Draw()
    for l in labels:
        l.SetTextSize(0.02)
        if args.labels:
            l.Draw()
        
    graph.SetTitle("Length ROC Plot")
    graph.GetXaxis().SetTitle("Background Acceptance (False Positive Rate)")
    graph.GetXaxis().SetLimits(0, 1)
    graph.GetYaxis().SetRangeUser(0, 1)
    graph.GetYaxis().SetTitle("Signal Acceptance")

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
    parser.add_argument("-l", "--labels", action="store_true")
    main(parser.parse_args())
