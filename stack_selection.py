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
    # get input file -- should be output from sbn -m SBNOsc_NuMuSelection
    input_file = ROOT.TFile(args.input)
    input_tree = input_file.Get("sbnana")
    # get the histos for the energy variable we care about
    (muon, pion) = build_histos(args, input_tree, args.observable)
    # plot them
    plot(args, muon, pion)

def build_histos(args, tree, observable_name):
    if args.variable_bins:
	muon_histo = ROOT.TH1D("muon_energy", "\mu+X CC", len(energy_bins) -1, energy_bins_array)
	pion_histo = ROOT.TH1D("pion_energy", "\pi+X NC", len(energy_bins) -1, energy_bins_array)
    else:
	muon_histo = ROOT.TH1D("muon_energy", "\mu+X CC", 100, float(args.minimum), float(args.supremum))
	pion_histo = ROOT.TH1D("pion_energy", "\pi+X NC", 100, float(args.minimum), float(args.supremum))
    for entry in tree:
        reco_interactions = entry.events.reco
        reco_info = entry.numu_interaction
        for (interaction, info) in zip(reco_interactions, reco_info):
            if hasattr(interaction.truth.neutrino, observable_name):
                observable = getattr(interaction.truth.neutrino, observable_name)
            elif hasattr(interaction, observable_name):
                observable = getattr(interaction, observable_name)
            elif hasattr(info, observable_name):
                observable = getattr(info, observable_name)
            else:
                assert(False)
            if args.diff_observable is not None:
		if hasattr(interaction.truth.neutrino, args.diff_observable):
		    diff_observable = getattr(interaction.truth.neutrino, args.diff_observable)
		elif hasattr(interaction, args.diff_observable):
		    diff_observable = getattr(interaction, args.diff_observable)
		elif hasattr(info, args.diff_observable):
		    diff_observable = getattr(info, args.diff_observable)
		else:
		    assert(False)
                observable -= diff_observable
            pdgid = info.t_pdgid
            if abs(pdgid) == 13:
                muon_histo.Fill(observable, args.constant)
            elif abs(pdgid) == 211:
                pion_histo.Fill(observable)
            else: 
                assert(False) # should only have muons and pions

    if args.normalize and args.variable_bins:
        for i,norm in zip(range(1, muon_histo.GetNbinsX()), energy_bin_sizes):
            muon_histo.SetBinContent(i, muon_histo.GetBinContent(i) / norm) 
            pion_histo.SetBinContent(i, pion_histo.GetBinContent(i) / norm)

    return muon_histo, pion_histo
        
def plot(args, muon_histo, pion_histo):
    # configure histos
    pion_histo.SetFillColor(30)
    muon_histo.SetFillColor(40)

    # make a stack
    hstack = ROOT.THStack("selection stack", "")
    hstack.Add(pion_histo)
    hstack.Add(muon_histo)
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 250,100,700,500)
    hstack.Draw("HIST")
    # configure stack
    if args.diff_observable is not None:
        hstack.GetXaxis().SetTitle("Neutrino Interaction (%s - %s) [%s]" % (args.observable, args.diff_observable, args.units))
    else:
        hstack.GetXaxis().SetTitle("Neutrino Interaction %s [%s]" % (args.observable, args.units))

    if args.normalize:
        hstack.GetYaxis().SetTitle("Events / %s" % args.units)
    else:
        hstack.GetYaxis().SetTitle("Events")

    # Legend
    legend = ROOT.gPad.BuildLegend(0.8,0.8,0.95,0.95,"")
    canvas.Update()
    if args.title is not None:
        title_text = ROOT.TPaveText(0.6, 0.5, 1.0, 0.75, "nbNDC")
        title_text.AddText(args.title)
        if args.pot is not None:
            title_text.AddText("POT: %.3E" % float(args.pot))
        title_text.SetLineColor(10)
        title_text.SetFillColor(10)
        title_text.Draw()
    canvas.Update()

    if args.wait:
        raw_input("Press Enter to continue...")

    if args.output is not None:
        canvas.SaveAs(args.output)

def float_or_file(arg):
    if arg is None:
        return None
    # first try to interpret as file
    if os.path.exists(arg):
        with open(arg) as f:
            text = f.readlines()
            dat = float(text[0].split(" ")[-1].rstrip("\n"))
    # then as float
    else:
        dat = float(arg)
    return dat

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
    parser.add_argument("-e", "--observable", default="energy")
    parser.add_argument("-s", "--supremum", default=10)
    parser.add_argument("-m", "--minimum", default=0)
    parser.add_argument("-t", "--title", default=None)
    parser.add_argument("-v", "--variable_bins", action="store_true")
    parser.add_argument("-p", "--pot", default=None, type=float_or_file)
    parser.add_argument("-c", "--constant", type=float, default=1.)
    parser.add_argument("-g", "--goal_pot", type=float_or_file, default=None)
    parser.add_argument("-n", "--normalize", action="store_true")
    parser.add_argument("-d", "--diff_observable", default=None)
    parser.add_argument("-u", "--units", default="")
    args = parser.parse_args()
    if args.pot is not None and args.goal_pot is not None:
        args.constant *= args.goal_pot / args.pot
    main(args)
