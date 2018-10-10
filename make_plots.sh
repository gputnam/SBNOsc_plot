#!/bin/bash
INDIR=$1
OUTDIR=$2

python cov_selection.py -o $OUTDIR/scaled_selection_SBND.pdf -i $INDIR/chi2_sr/cov.root -d 0 -t "SBND Scaled MC" -p 6.6e20 -s
python cov_selection.py -o $OUTDIR/scaled_selection_Uboone.pdf -i $INDIR/chi2_sr/cov.root -d 1 -t "MicroBooNE Scaled MC" -p 1.32e21 -s
python cov_selection.py -o $OUTDIR/scaled_selection_Icarus.pdf -i $INDIR/chi2_sr/cov.root -d 2 -t "ICARUS Scaled MC" -p 6.6e20 -s

python stack_selection.py -u GeV -e reco_energy -o $OUTDIR/stack_reco_energy_icarus.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Icarus.root -t "ICARUS Unscaled MC" -p $INDIR/ICARUS_POT
python stack_selection.py -u GeV -e reco_energy -o $OUTDIR/stack_reco_energy_sbnd.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_SBND.root -t "SBND Unscaled MC" -p $INDIR/SBND_POT
python stack_selection.py -u GeV -e reco_energy -o $OUTDIR/stack_reco_energy_uboone.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Uboone.root -t "MicroBooNE Unscaled MC" -p $INDIR/UBOONE_POT

python stack_selection.py -u cm -e t_length -o $OUTDIR/stack_t_length_icarus.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Icarus.root -s 1000 -t "ICARUS Unscaled MC" -p $INDIR/ICARUS_POT
python stack_selection.py -u cm -e t_length -o $OUTDIR/stack_t_length_sbnd.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_SBND.root -s 1000 -t "SBND Unscaled MC" -p $INDIR/SBND_POT
python stack_selection.py -u cm -e t_length -o $OUTDIR/stack_t_length_uboone.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Uboone.root -s 1000 -t "MicroBooNE Unscaled MC" -p $INDIR/UBOONE_POT

python stack_selection.py -u GeV -e eccqe -o $OUTDIR/stack_eccqe_icarus.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Icarus.root -t "ICARUS Unscaled MC" -p $INDIR/ICARUS_POT
python stack_selection.py -u GeV -e eccqe -o $OUTDIR/stack_eccqe_sbnd.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_SBND.root -t "SBND Unscaled MC" -p $INDIR/SBND_POT
python stack_selection.py -u GeV -e eccqe -o $OUTDIR/stack_eccqe_uboone.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Uboone.root -t "MicroBooNE Unscaled MC" -p $INDIR/UBOONE_POT

python stack_selection.py -u GeV -e energy -o $OUTDIR/stack_energy_icarus.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Icarus.root -t "ICARUS Unscaled MC" -p $INDIR/ICARUS_POT
python stack_selection.py -u GeV -e energy -o $OUTDIR/stack_energy_sbnd.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_SBND.root -t "SBND Unscaled MC" -p $INDIR/SBND_POT
python stack_selection.py -u GeV -e energy -o $OUTDIR/stack_energy_uboone.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Uboone.root  -t "MicroBooNE Unscaled MC" -p $INDIR/UBOONE_POT


python cut_graph.py -o $OUTDIR/cut_graph_icarus.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Icarus.root
python cut_graph.py -o $OUTDIR/cut_graph_sbnd.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_SBND.root
python cut_graph.py -o $OUTDIR/cut_graph_uboone.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_Uboone.root


# python stack_selection.py -wvn -g 6.6e20 -p ../gputnam_newLarsim_sample/ICARUS_POT -c 1 -e reco_energy -i ../gputnam_newLarsim_sample/output_SBNOsc_NumuSelection_Proposal_Icarus.root
