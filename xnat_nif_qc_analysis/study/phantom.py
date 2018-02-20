from nianalysis.data_formats import dicom_format, nifti_format, nifti_gz_format
from nianalysis.study.base import set_data_specs, Study
from nianalysis.interfaces.mrtrix import MRConvert
from nianalysis.requirements import mrtrix3_req
from nianalysis.dataset import DatasetSpec, FieldSpec
from xnat_nif_qc_analysis.interface.qc import QCMetrics


class PhantomStudy(Study):

    default_options = {
        't1_32ch': {
            't1_32ch_threshold': 0.25,
            't1_32ch_signal_radius': 0.8,
            't1_32ch_ghost_radii': (1.1, 1.5),
            't1_32ch_background_radius': 1.8,
            't1_32ch_z_extent': 0.5},
        't2_32ch': {
            't2_32ch_threshold': 0.25,
            't2_32ch_signal_radius': 0.8,
            't2_32ch_ghost_radii': (1.1, 1.5),
            't2_32ch_background_radius': 1.8,
            't2_32ch_z_extent': 0.5},
        'dmri_32ch': {
            'dmri_32ch_threshold': 0.25,
            'dmri_32ch_signal_radius': 0.8,
            'dmri_32ch_ghost_radii': (1.1, 1.5),
            'dmri_32ch_background_radius': 1.8,
            'dmri_32ch_z_extent': 0.5}}

    def t1_32ch_qc_metrics_pipeline(self, **options):
        return self.qc_metrics_pipeline_factory(
            't1_32ch_saline', 't1_32ch', **options)

    def t2_32ch_qc_metrics_pipeline(self, **options):
        return self.qc_metrics_pipeline_factory(
            't2_32ch_saline', 't2_32ch', **options)

    def dmri_32ch_qc_metrics_pipeline(self, **options):
        return self.qc_metrics_pipeline_factory(
            'dmri_b0_32ch_saline', 'dmri_32ch', **options)

    def qc_metrics_pipeline_factory(self, input, contrast, **options):  # @ReservedAssignment @IgnorePep8
        def prefix(name):
            return contrast + '_' + name
        pipeline = self.create_pipeline(
            name=prefix('qc_metrics'),
            inputs=[DatasetSpec(input, nifti_format)],
            outputs=[FieldSpec(prefix('snr'), dtype=float),
                     FieldSpec(prefix('uniformity'), dtype=float),
                     FieldSpec(prefix('ghost_intensity'), dtype=float),
                     DatasetSpec(prefix('signal'), format=nifti_format),
                     DatasetSpec(prefix('ghost'), format=nifti_format),
                     DatasetSpec(prefix('background'), format=nifti_format)],
            description="Registers a MR scan against a reference image",
            default_options=self.default_options[contrast],
            version=1,
            citations=[],
            options=options)
        metrics = pipeline.create_node(interface=QCMetrics(),
                                       name=prefix('metrics'), wall_time=5)
        metrics.inputs.threshold = pipeline.option(prefix('threshold'))
        metrics.inputs.signal_radius = pipeline.option(prefix('signal_radius'))
        metrics.inputs.ghost_radii = pipeline.option(prefix('ghost_radii'))
        metrics.inputs.background_radius = pipeline.option(
            prefix('background_radius'))
        metrics.inputs.z_extent = pipeline.option(prefix('z_extent'))
        # Connect inputs
        pipeline.connect_input(input, metrics, 'in_file')
        # Connect outputs
        pipeline.connect_output(prefix('snr'), metrics, 'snr')
        pipeline.connect_output(prefix('uniformity'), metrics, 'uniformity')
        pipeline.connect_output(prefix('ghost_intensity'), metrics,
                                'ghost_intensity')
        pipeline.connect_output(prefix('signal'), metrics, 'signal')
        pipeline.connect_output(prefix('ghost'), metrics, 'ghost')
        pipeline.connect_output(prefix('background'), metrics, 'background')
        pipeline.assert_connected()
        return pipeline

    def b0_32ch_extraction_pipeline(self, **options):
        pipeline = self.create_pipeline(
            name='epi_extraction',
            inputs=[DatasetSpec('dmri_32ch_saline', dicom_format)],
            outputs=[DatasetSpec('dmri_b0_32ch_saline', nifti_gz_format)],
            description=(
                "Extracts the first b0 image from the dmri sequence"),
            default_options={},
            version=1,
            citations=[],
            options=options)
        mrconvert = pipeline.create_node(interface=MRConvert(),
                                         name='mrconvert',
                                         requirements=[mrtrix3_req])
        mrconvert.inputs.coord = (3, 0)
        mrconvert.inputs.axes = '0,1,2'
        mrconvert.inputs.out_ext = '.nii.gz'
        pipeline.connect_input('dmri_32ch_saline', mrconvert,
                               'in_file')
        pipeline.connect_output('dmri_b0_32ch_saline', mrconvert,
                                'out_file')
        pipeline.assert_connected()
        return pipeline

    _data_specs = set_data_specs(
        DatasetSpec('t1_32ch_saline', dicom_format),
        DatasetSpec('t2_32ch_saline', dicom_format),
        DatasetSpec('dmri_32ch_saline', dicom_format),
        DatasetSpec('dmri_b0_32ch_saline', format=nifti_gz_format,
                    pipeline=b0_32ch_extraction_pipeline),
        DatasetSpec('t1_32ch_signal', format=nifti_gz_format,
                    pipeline=t1_32ch_qc_metrics_pipeline),
        DatasetSpec('t1_32ch_ghost', format=nifti_gz_format,
                    pipeline=t1_32ch_qc_metrics_pipeline),
        DatasetSpec('t1_32ch_background', format=nifti_gz_format,
                    pipeline=t1_32ch_qc_metrics_pipeline),
        FieldSpec('t1_32ch_snr', dtype=float,
                  pipeline=t1_32ch_qc_metrics_pipeline),
        FieldSpec('t1_32ch_uniformity', dtype=float,
                  pipeline=t1_32ch_qc_metrics_pipeline),
        FieldSpec('t1_32ch_ghost_intensity', dtype=float,
                  pipeline=t1_32ch_qc_metrics_pipeline),
        DatasetSpec('t2_32ch_signal', format=nifti_gz_format,
                    pipeline=t2_32ch_qc_metrics_pipeline),
        DatasetSpec('t2_32ch_ghost', format=nifti_gz_format,
                    pipeline=t2_32ch_qc_metrics_pipeline),
        DatasetSpec('t2_32ch_background', format=nifti_gz_format,
                    pipeline=t2_32ch_qc_metrics_pipeline),
        FieldSpec('t2_32ch_snr', dtype=float,
                  pipeline=t2_32ch_qc_metrics_pipeline),
        FieldSpec('t2_32ch_uniformity', dtype=float,
                  pipeline=t2_32ch_qc_metrics_pipeline),
        FieldSpec('t2_32ch_ghost_intensity', dtype=float,
                  pipeline=t2_32ch_qc_metrics_pipeline),
        DatasetSpec('dmri_32ch_signal', format=nifti_gz_format,
                    pipeline=dmri_32ch_qc_metrics_pipeline),
        DatasetSpec('dmri_32ch_ghost', format=nifti_gz_format,
                    pipeline=dmri_32ch_qc_metrics_pipeline),
        DatasetSpec('dmri_32ch_background', format=nifti_gz_format,
                    pipeline=dmri_32ch_qc_metrics_pipeline),
        FieldSpec('dmri_32ch_snr', dtype=float,
                  pipeline=dmri_32ch_qc_metrics_pipeline),
        FieldSpec('dmri_32ch_uniformity', dtype=float,
                  pipeline=dmri_32ch_qc_metrics_pipeline),
        FieldSpec('dmri_32ch_ghost_intensity', dtype=float,
                  pipeline=dmri_32ch_qc_metrics_pipeline))


# mrconvert RL.mif -coord 3 0
