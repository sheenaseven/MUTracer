# MUTracer


<div align=center><img width="300" src="logo.png" style="display: block; margin: auto;" ></div>

## Ownership

[Wang Lab at HKUST](http://wang-lab.ust.hk/)

## Status

Active Development

## Introduction

MUTracer is a variant calling protocol for specifically characterize the somatic mutations in Cerebral Cavernous Malformation patients. 

## Prerequisites

• SAVI2 report.coding.PDfilter.txt and report.coding.txt

## Workflow

### Step 1: Screen somatic mutations 

Starting from report.coding.PDfilter.txt file, **screenSomaticMutation.py** generates filtered somatic candidates based on the following criteria: (1) variant allele frequency in blood samples no more than 1% (BLO_freq ≤ 1%); (2) S1_alt_depth_per_position no more than 1; (3) P-value for strand bias in CCM tissue (strand_bias_CCM) ≥ 0.01, alt_forward_depth_CCM > 0, and alt_reverse_depth_CCM > 0; (4) not in Meganormal database; (5) not common SNPs; (6) non-synonymous mutations; (7) Amino_Acid_length ≤ 2000. 

```
usage: screenSomaticMutation.py [-h] [-b BLOVAF] [-n NORMALALT] [-s STRANDBIAS]
                                [-f ALTFOR] [-r ALTREV] [-m MEGA] [-c COMSNP]
                                [-a ALTTYPE] [-l AALENGTH] [-o OUTPUTDIR] inputPDfilter

positional arguments:
  inputPDfilter         The txt file (report.coding.PDfilter.txt) obtained from SAVI2.

optional arguments:
  -h, --help            show this help message and exit
  -b BLOVAF             The maximum variant allele frequency in blood samples. 
                        Default: 1% (i.e. ≤ 1%)
  -n NORMALALT          The maximum number of altered reads detected at that 
                        position in blood samples. Default: 1 (i.e. ≤ 1)
  -s STRANDBIAS         The minmum p-value for strand bias in CCM tissue. 
                        Default: 0.01 (i.e. ≥ 0.01)
  -f ALTFOR             The least number of alter forward depth in CCM tissue, 
                        Default: 0 (i.e. > 0)
  -r ALTREV             The least number of alter reverse depth in CCM tissue, 
                        Default: 0 (i.e. > 0)
  -m MEGA               whether exclude the mutation which is reported in Meganormal
                        database. Default: True
  -c COMSNP             whether exclude the mutation which is common SNP.
                        Default: True
  -a ALTTYPE            remove the candidates with specific mutation type. 
                        Default: synonymous mutations
  -l AALENGTH           The maximum number of screen Amino Acid length. 
                        Default: 2000 (i.e. ≤ 2000)
  -o OUTPUTDIR          output directory for the output files

```

Example:
```
python screenSomaticMutation.py Input_SAVI_PDfilter.txt
```
**Note:** the column name of Input_SAVI_PDfilter.txt should be the same as Input_SAVI_PDfilter_column_name.txt.

### Step 2: Prioritize somatic mutations 

After step 1, the mutated genes can be collected. Then STRING database was then employed to prioritize these genes that are related with CCM1, CCM2, CCM3 and MAP3K3. Finally, screen candidates with mutations in prioritized genes.

### Step 3: Re-examine potential low-frequency somatic mutations 

Recheck the report.coding.txt including the candidates with mutations in prioritized genes (Step 2).


28 Feb 2021

