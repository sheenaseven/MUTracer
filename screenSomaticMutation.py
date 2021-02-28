import pandas as pd
import sys
import argparse as ag
import os


parser = ag.ArgumentParser(prog='screenSomaticMutation',
                           description='a variant calling protocol for specifically characterize the somatic mutations in Cerebral Cavernous Malformation patients')
parser.add_argument('-b',dest='BLOVAF',required=False, default=1, type=float,
                    help='set the maximum variant allele frequency in blood samples; default: %(default)s (i.e. <=1)')
parser.add_argument('-n',dest='NORMALALT',required=False, default=1, type=float,
                    help='set the maximum of altered reads detected at that position in blood samples; default: %(default)s (i.e. <=1)')
parser.add_argument('-s',dest='STRANDBIAS',required=False, default=0.01, type=float,
                    help='set the minimum p-value for strand bias in CCM tissue; default: %(default)s (i.e. >=0.01)')
parser.add_argument('-f',dest='ALTFOR',required=False, default=0, type=float,
                    help='set the minimum alter forward depth in CCM tissue; default: %(default)s (i.e. >0)')
parser.add_argument('-r',dest='ALTREV',required=False, default=0, type=float,
                    help='set the minimum alter reverse depth in CCM tissue; default: %(default)s (i.e. >0)')
parser.add_argument('-m',dest='MEGA',required=False, default=True, type=bool,
                    help='whether exclude the mutation which is reported in Meganormal database; default: %(default)s')
parser.add_argument('-c',dest='COMSNP',required=False, default=True, type=bool,
                    help='whether exclude the mutation which is common SNP; default: %(default)s')
parser.add_argument('-a',dest='ALTTYPE',required=False, default='synonymous_variant', type=str,
                    help='remove the candidates with specific mutation type; default: %(default)s')
parser.add_argument('-l',dest='AALENGTH',required=False, default=2000, type=int,
                    help='set the maximum Amino Acid length; default: %(default)s (i.e. <=2000)')
parser.add_argument('-o',dest='OUTPUTDIR',required=False, default='./', type=str,
                    help='output directory for the output files; default: %(default)s')
parser.add_argument('-N',dest='OUTPUTNAME',required=False, default='MUTracer_result.txt', type=str,
                    help='output filename for the output files; default: %(default)s')
parser.add_argument("inputPDfilter", nargs=1, default='',type=str,
                    help='The txt file (report.coding.PDfilter.txt) obtained from SAVI2')

args = parser.parse_args()

input_dir = args.inputPDfilter[0]

output_dir = args.OUTPUTDIR.strip('/')
name = args.OUTPUTNAME
b = args.BLOVAF
n = args.NORMALALT
s = args.STRANDBIAS
f = args.ALTFOR
r = args.ALTREV
m = args.MEGA
c = args.COMSNP
a = args.ALTTYPE
l = args.AALENGTH

if not os.path.isfile(input_dir):
    sys.exit('Path to input file is not valid!')
if not os.path.isdir(output_dir):
    sys.exit('Path to save output is not valid!')

input = pd.read_csv(input_dir,sep='\t')
res = input

res = res[res['BLO_freq']<=b]
res = res[res['S1_alt_depth_per_position']<=n]
res = res[res['strand_bias_CCM']>=s]
res = res[res['alt_forward_depth_CCM']>f]
res = res[res['alt_reverse_depth_CCM']>r]
if m:
    res = res[res['meganormal_id']=='-']
    res = res[res['meganormal_186_TCGA_source'] == '-']
if c:
    res = res[~res['snp.common'].str.contains('1')]

res = res[~res['Effect'].str.contains('synonymous_variant')]

res['Amino_Acid_length'] = [int(str(i).split(',')[0]) for i in res['Amino_Acid_length']]
res = res[res['Amino_Acid_length']<=l]

res.to_csv(output_dir+'/'+name,sep='\t', index=None)
print('screenSomaticMutation has finished!')

