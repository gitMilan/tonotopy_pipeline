Tonotopy pipeline

This snakemake pipeline is used to create tonotopic images using data from fmri experiments.
More information can be found in the paper "Mapping the Tonotopic Organization in Human Auditory Cortex with Minimally Salient
Acoustic Stimulation" written by Dave R.M. Langers and Pim van Dijk.


Instructions:

1) Create and run a virtualenv

2) Install required packages:
pip install -r requirements.txt

3) Modify config.yaml to point the 'tonotopy_data' entry to the Tonotopy data, if left unchanged
the 2 included samples are used.

4) run in shell:
snakemake -c <number of cores>

5) View the created tonotopic map, found at plots/tonotopic_map.png




