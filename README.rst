XNAT NIF QC Analysis Pipeline
=============================

This pipeline performs basic analysis on QC data acquired in accordance
with the National Imaging Facility's (NIF) "Trusted Data Repository"
standard operating procedure, saving the metrics as "custom variables"
in the processed XNAT pipeline.

Metrics
-------

The analysis pipeline extracts the following metrics (see NIF QC SOP
for formal definition)

* SNR
* Uniformity
* Ghost Intensity

for three imaging contrasts

* T1-weighted MPRAGE
* T2-weighted SPACE
* diffusion MR EPI

