from neuroconv import NWBConverter
from kpms2nwb.kpmsdatainterface import KeypointMoseqSubjectDataInterface
import keypoint_moseq as kpms
import datetime

# ---- Set up NWBConverter and directory parameters

class ExampleKpmsNWBConverter(NWBConverter):
    data_interface_classes = dict(
        KeypointMoseq=KeypointMoseqSubjectDataInterface,
    )

model_folder = 'kpms_model'
project_dir = '../data/tut/demo_project/'
nwb_path_fmt = '../data/converted/{session}.nwb'


config = lambda: kpms.load_config(project_dir)


# ---- Run conversion for each sesssion in the results file

for session_name in KeypointMoseqSubjectDataInterface.list_sessions(project_dir, model_folder):
    print("> Converting session:", session_name)

    source_data = dict(
        KeypointMoseq=dict(
            project_dir = project_dir,
            model_folder = model_folder,
            session_name = session_name,
            **KeypointMoseqSubjectDataInterface.metadata_from_config(**config())
        )
    )
    converter = ExampleKpmsNWBConverter(source_data = source_data)

    metadata = converter.get_metadata()
    metadata["NWBFile"]['session_description'] = "Open-field behavior session from keypoint-moseq tutorial dataset."
    metadata["NWBFile"]['identifier'] = session_name
    metadata["NWBFile"]['session_start_time'] = datetime.datetime.now(datetime.timezone.utc)
    metadata["BehavioralSyllable"]['kpms_version'] = kpms.__version__

    converter.run_conversion(
        metadata = metadata,
        nwbfile_path = nwb_path_fmt.format(session = session_name))