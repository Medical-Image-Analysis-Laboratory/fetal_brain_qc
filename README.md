# Fetal Brain Quality Control
## About
![fetal brain QC](fetal_brain_qc.png)

*Fetal brain QC* is a tool to facilitate quality annotations of T2w fetal brain MRI images, by creating interactive html-based visual reports from fetal brain scans. It uses a pair of low-resolution (LR) T2w images with corresponding brain masks to provide snapshots of the brain in the three orientations of the acquisition in the subject-space. 

The code is based on MRIQC [1], available at https://github.com/nipreps/mriqc.

**Note.** The current version of *Fetal brain QC* only works on low-resolution T2w images.

**Disclaimer.** Fetal brain QC is not intended for clinical use.


## Installation
fetal_brain_qc was developed in Ubuntu 22.04 and tested for python 3.9.12

To install this repository, first clone it via
```
git@github.com:Medical-Image-Analysis-Laboratory/fetal_brain_qc.git
```

Move then into the repository and install the remaining dependencies using pip
```
pip install -e .
```

## Usage
*Fetal brain QC* starts from a [BIDS](https://bids.neuroimaging.io/) dataset (containing `NIfTI` formatted images), as well as an additional folder containing *brain masks*. 

The recommended workflow is to use `qc_run_pipeline`
```
usage: qc_run_pipeline [-h] [--mask-patterns MASK_PATTERNS [MASK_PATTERNS ...]] [--bids-csv BIDS_CSV] [--anonymize-name | --no-anonymize-name] [--randomize | --no-randomize] [--seed SEED]
                       [--n-reports N_REPORTS] [--n-raters N_RATERS]
                       bids-dir out-path

Given a `bids_dir`, lists the LR series in the directory and tries to find corresponding masks given by `mask_patterns`. Then, saves all the found pairs of (LR series, masks) in a CSV file at `bids_csv`

positional arguments:
  bids-dir              BIDS directory containing the LR series.
  out-path              Path where the reports will be stored.

optional arguments:
  -h, --help            show this help message and exit
  --mask-patterns MASK_PATTERNS [MASK_PATTERNS ...]
                        List of patterns to find the LR masks corresponding to the LR series. Patterns will be of the form
                        "sub-{subject}[/ses-{session}][/{datatype}]/sub-{subject}[_ses-{session}][_acq-{acquisition}][_run-{run}]_{suffix}.nii.gz", and the different fields will be substituted based on
                        the structure of bids_dir. The code will attempt to find the mask corresponding to the first pattern, and if it fails, will attempt the next one, etc. If no masks are found, a
                        warning message will be displayed for the given subject, session and run. (default: ['/media/tsanchez/tsanchez_data/data/data_anon/derivatives/refined_masks/sub-{subject}[/ses-{
                        session}][/{datatype}]/sub-{subject}[_ses-{session}][_acq-{acquisition}][_run-{run}]_{suffix}.nii.gz', '/media/tsanchez/tsanchez_data/data/data_anon/derivatives/automated_masks/
                        sub-{subject}[/ses-{session}][/{datatype}]/sub-{subject}[_ses-{session}][_acq-{acquisition}][_run-{run}]_{suffix}.nii.gz'])
  --bids-csv BIDS_CSV   CSV file where the list of available LR series and masks is stored. (default: bids_csv.csv)
  --anonymize-name, --no-anonymize-name
                        Whether an anonymized name must be stored along the paths in `out-csv`. This will determine whether the reports will be anonymous in the end. (default: True)
  --randomize, --no-randomize
                        Whether the order of the reports should be randomized. The number of splits will be given by `n-raters` and the number of reports in each split by `n-reports`. The results will
                        be stored in different subfolders of `out-path` (default: True)
  --seed SEED           Seed to control the randomization (to be used with randomize=True). (default: 42)
  --n-reports N_REPORTS
                        Number of reports that should be used in the randomized study (to be used with randomize=True). (default: 100)
  --n-raters N_RATERS   Number of permutations of the data that must be computed (to be used with randomize=True). (default: 3)
```
**Remark.** This script runs the whole pipeline of *fetal brain QC*, i.e. listing of BIDS directory and masks -> (anonymization of data) -> report generation (-> randomization of reports) -> index file generation


```
qc_generate_index [-h] [--report-path REPORT_PATH]
                         [--add-script-to-reports | --no-add-script-to-reports]

options:
  -h, --help            show this help message and exit
  --report-path REPORT_PATH
                        Path where the reports are located
  --add-script-to-reports, --no-add-script-to-reports
                        Whether some javascript should be added to the report for interaction with
                        the index file. (default: True)
```

```
usage: qc_generate_reports [-h] [-o OUT_PATH] [--bids-csv BIDS_CSV] [--add-js | --no-add-js]

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_PATH, --out-path OUT_PATH
                        Path where the reports will be stored.
  --bids-csv BIDS_CSV   Path where the bids config csv file is located.
  --add-js, --no-add-js
                        Whether some javascript should be added to the report for interaction with the index file. (default: True)
```

## References
[1] Esteban, Oscar, et al. "MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites." PloS one 12.9 (2017): e0184661.