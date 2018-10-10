import ROOT
import os
import sys
from array import array
import argparse
import math

energy_bins = [0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1. , 1.25, 1.5, 2., 2.5, 3.] 

energy_centers = []
energy_bin_sizes = []
for i in range(len(energy_bins) - 1):
    energy_centers.append( (energy_bins[i] + energy_bins[i+1]) / 2.)
    energy_bin_sizes.append( energy_bins[i+1] - energy_bins[i])

energy_bins_array = array('d', energy_bins)
energy_bin_centers_array = array('d', energy_centers)

def main(args):
    # global config
    ROOT.TGaxis.fgMaxDigits = 3
    # get input file -- should be output from sbn -m SBNOsc_NuMuSelection
    input_file = ROOT.TFile(args.input)
    # get (2D) signal histogram
    signal_hist = input_file.Get("Neutrinos")
    # get (1D) background histogram
    bkg_hist =  input_file.Get("Background")
    # get covariance matrix
    cov = input_file.Get("cov")

    # extract this detector from full hist
    (sig_proj, sig_hist, bkg_hist) = extract_histo(signal_hist, bkg_hist, args.detector, args.scale_bins)
    # get error bars
    (stat_err, tot_err) = calculate_errors(sig_hist, bkg_hist, cov, args.detector)

    # plot them
    plot(args, sig_hist, bkg_hist, stat_err, tot_err)

def extract_histo(sig_hist, bkg_hist, detector_index, scale_bins):
    sig_out = ROOT.TH1D("sig", "\mu+X CC", len(energy_bins)-1, energy_bins_array) 
    bkg_out = ROOT.TH1D("bkg", "\pi+X NC", len(energy_bins)-1, energy_bins_array)

    sig_proj = sig_hist.ProjectionY()

    # fill up signal and bkg
    for i in range(len(energy_bins)-1):
        sig = sig_proj.GetBinContent(i+1 + detector_index * (len(energy_bins)-1))
        bkg = bkg_hist.GetBinContent(i+1 + detector_index * (len(energy_bins)-1))
        if scale_bins:
            sig /= energy_bin_sizes[i]
            bkg /= energy_bin_sizes[i]
        sig_out.SetBinContent(i+1, sig)
        bkg_out.SetBinContent(i+1, bkg)

    return (sig_proj, sig_out, bkg_out)

def calculate_errors(sig_hist, bkg_hist, cov, detector_index):
    x = energy_bin_centers_array
    y = array('d')
    for i in range(1, len(energy_bins)):
        y.append(sig_hist.GetBinContent(i) + bkg_hist.GetBinContent(i))
    stat_err = array('d', [math.sqrt(yval) for yval in y])
    tot_err = array('d')
    
    base_cov_ind = 1 + detector_index * (len(energy_bins)-1) 
    for i in range(len(energy_bins)-1):
        cov_ind = i + base_cov_ind
        this_syst_err = cov.GetBinContent(cov_ind, cov_ind)
        this_tot_err = math.sqrt(this_syst_err + y[i])
        tot_err.append(this_tot_err)

    errx = array('d', [0 for i in range(len(energy_bins) -1)])

    stat_err_graph = ROOT.TGraphErrors(len(y), x, y, errx, stat_err)
    tot_err_graph = ROOT.TGraphErrors(len(y), x, y, errx, tot_err)

    print stat_err
    print tot_err
    return (stat_err_graph, tot_err_graph)


def plot(args, sig_hist, bkg_hist, stat_err, tot_err):
    # configure histos
    bkg_hist.SetFillColor(30)
    sig_hist.SetFillColor(40) 
    
    # make a stack
    hstack = ROOT.THStack("selection stack", "")
    hstack.Add(bkg_hist)
    hstack.Add(sig_hist)
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 450, 600)
    canvas.SetLeftMargin(0.22)
    canvas.SetBottomMargin(0.12)

    hstack.Draw()
    # configure stack
    hstack.GetXaxis().SetTitle("Smeared Visible Energy [GeV]")
    if args.scale_bins:
        hstack.GetYaxis().SetTitle("Entries/GeV")
    else:
        hstack.GetYaxis().SetTitle("Entries")

    #ROOT.gStyle.SetLabelSize(2, "XY")
    hstack.GetXaxis().SetLabelSize(0.06)
    hstack.GetYaxis().SetLabelSize(0.06)
    hstack.GetXaxis().SetTitleSize(0.06)
    hstack.GetYaxis().SetTitleSize(0.06)
   

    # draw stat and tot err
    if args.errors:
        stat_err.Draw("SAMEap")
        tot_err.Draw("SAMEap")

    # Legend
    legend = ROOT.gPad.BuildLegend(0.6,0.75,0.95,0.95,"")
    legend.SetTextSize(0.06)
    canvas.Update()
    if args.title is not None:
        title_text = ROOT.TPaveText(0.55, 0.4, 0.95, 0.65, "nbNDC")
        title_text.AddText(args.title)
        if args.pot is not None:
            title_text.AddText("POT: %.2E" % float(args.pot))
        title_text.SetLineColor(10)
        title_text.SetFillColor(10)
        title_text.Draw()
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
    parser.add_argument("-t", "--title", default=None)
    parser.add_argument("-p", "--pot", default=None)
    parser.add_argument("-d", "--detector", default=0, type=int)
    parser.add_argument("-e", "--errors", action="store_true")
    parser.add_argument("-s", "--scale_bins", action="store_true")
    main(parser.parse_args())
