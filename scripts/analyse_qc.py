#!/usr/bin/env python
"""
Script to automatically analyse QC data acquiried according to the NIF
TDRS SOP.
"""
import os.path
from collections import defaultdict
from argparse import ArgumentParser
from nianalysis.dataset import Dataset
from nianalysis.archive.xnat import XNATArchive
from nianalysis.data_formats import dicom_format
from xnat_nif_qc_analysis.study.phantom import PhantomStudy

AVAIL_OPTIONS = [
    'threshold',
    'signal_radius',
    'ghost_radii',
    'background_radius',
    'z_extent']

AVAIL_PHANTOMS = [
    't1_32ch',
    't2_32ch',
    'dmri_32ch']

# t1_32ch_saline t1_mprage_trans_p2_iso_0.9_32CH
# t2_32ch_saline t2_spc_tra_iso_32CH
# dmri_32ch_saline ep2d_diff_mddw_12_p2_32CH

parser = ArgumentParser(__doc__)
parser.add_argument('server', type=str,
                    help="The XNAT server to analysis the QC data for")
parser.add_argument('--phantom', '-p', nargs=2, action='append',
                    type=str, default=[],
                    metavar=['PHANTOM', 'SCAN_NAME'],
                    help=("Phantoms to analyse run (available: "
                          "'{}')".format("', '".join(AVAIL_PHANTOMS))))
parser.add_argument('--instruments', '-i', nargs='+', default=None,
                    help=("The instruments to process QC data for "
                          "(defaults to all)"))
parser.add_argument('--dates', '-d', nargs='+', type=str,
                    default=None, help=(
                        "Dates (in YYYYMMDD format) of the QC "
                        "acquisitions to process (defaults to all)"))
parser.add_argument('--reprocess', default=False, action='store_true',
                    help="Whether to reprocess the metrics")
parser.add_argument('--option', '-o', nargs=3, action='append',
                    metavar=['PHANTOM', 'NAME', 'VALUE'], default=[],
                    help=("Change a pipeline option from the default "
                          "(available options: '{}')".format(
                              "', '".join(AVAIL_OPTIONS))))
args = parser.parse_args()

# Create phantom study
qc_study = PhantomStudy(
    name='qc',
    project_id='INSTRUMENT',
    archive=XNATArchive(server=args.server),
    inputs=dict(('{}_saline'.format(n), Dataset(s, dicom_format))
                for n, s in args.phantom))

options = defaultdict(dict)
for phantom, name, value in args.option:
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass
    options[phantom][name] = value

instruments = (['INSTRUMENT_{}'.format(i)
               for i in args.instruments]
               if args.instruments is not None else None)

for phantom, _ in args.phantom:
    pipeline_getter = getattr(qc_study,
                              phantom + '_qc_metrics_pipeline')
    pipeline_getter(**options[phantom]).run(
        subject_ids=instruments,
        visit_ids=args.dates,
        reprocess=('all' if args.reprocess else False),
        work_dir=os.path.join(os.path.dirname(__file__), '..',
                              'test', 'data', 'work', 'analyze_qc'))
