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
    # get the histos for the energy variable we care about
    (muon, pion) = build_histos(input_tree, args.energy)
    # plot them
    plot(args, muon, pion)

def build_histos(tree, energy_name):
    muon_histo = ROOT.TH1D("muon_energy", "\mu^+ CC", 100, 0, 10)
    pion_histo = ROOT.TH1D("pion_energy", "\pi^+ NC", 100, 0, 10)
    for entry in tree:
        reco_interactions = entry.events.reco
        reco_info = entry.numu_interaction
        for (interaction, info) in zip(reco_interactions, reco_info):
            energy = getattr(interaction.truth.neutrino, energy_name)
            pdgid = info.t_pdgid
            if pdgid == 13:
                muon_histo.Fill(energy)
            elif abs(pdgid) == 211:
                pion_histo.Fill(energy)
            else: 
                assert(False) # should only have muons and pions
    return muon_histo, pion_histo
        
def plot(args, muon_histo, pion_histo):
    # configure histos
    pion_histo.SetFillColor(ROOT.kRed)
    muon_histo.SetFillColor(ROOT.kBlue)

    # make a stack
    hstack = ROOT.THStack("selection stack", "")
    hstack.Add(pion_histo)
    hstack.Add(muon_histo)
    canvas = ROOT.TCanvas("canvas", "Selection Canvas", 250,100,700,500)
    hstack.Draw()
    # configure stack
    hstack.GetXaxis().SetTitle("Neutrino Energy (%s) [GeV]" % args.energy)
    hstack.GetYaxis().SetTitle("NEntries")

    # Legend
    ROOT.gPad.BuildLegend(0.75,0.75,0.95,0.95,"")
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
    parser.add_argument("-e", "--energy", default="energy")
    main(parser.parse_args())
