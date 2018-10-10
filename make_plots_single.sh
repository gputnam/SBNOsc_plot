#!/bin/bash
DETECTOR=$1
INDIR=$2
OUTDIR=$3

POT="6.6e20"
if [ $DETECTOR == "uboone" ]
then
  POT="1.32e21"
fi


python stack_selection.py -u GeV -vn -g $POT -p $INDIR/${DETECTOR^^}_POT -c 0.8 -e reco_energy -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root -o $OUTDIR/scaled_reco_stack.pdf

python stack_selection.py -u GeV -e reco_energy -o $OUTDIR/stack_reco_energy_${DETECTOR}.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root -t "${DETECTOR} Unscaled MC" -p $INDIR/${DETECTOR^^}_POT

python stack_selection.py -u cm -e t_length -o $OUTDIR/stack_t_length_${DETECTOR}.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root -s 1000 -t "${DETECTOR} Unscaled MC" -p $INDIR/${DETECTOR^^}_POT

python stack_selection.py -u GeV -e eccqe -o $OUTDIR/stack_eccqe_${DETECTOR}.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root -t "${DETECTOR} Unscaled MC" -p $INDIR/${DETECTOR^^}_POT

python stack_selection.py -u GeV -e energy -o $OUTDIR/stack_energy_${DETECTOR}.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root -t "${DETECTOR} Unscaled MC" -p $INDIR/${DETECTOR^^}_POT

python cut_graph.py -o $OUTDIR/cut_graph_${DETECTOR}.pdf -i $INDIR/output_SBNOsc_NumuSelection_Proposal_${DETECTOR}.root

