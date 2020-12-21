from nwb_conversion_tools import NWBConverter, CEDRecordingInterface
from .heidelberg_ophys_interface import HeidelbergOphysInterface
# from .heidelberg_ecephys_interface import HeidelbergEcephysInterface


class HeidelbergNWBConverter(NWBConverter):

    # Modular data interfaces
    data_interface_classes = {
        # 'HeidelbergEcephysInterface': HeidelbergEcephysInterface,
        'CEDRecordingInterface': CEDRecordingInterface,
        'HeidelbergOphysInterface': HeidelbergOphysInterface,
    }

    def __init__(self, source_data):
        channel_info = CEDRecordingInterface.get_all_channels_info(source_data['CEDRecordingInterface']['file_path'])
        rhd_channels = []
        for ch, info in channel_info.items():
            if "Rhd" in info["title"]:
                rhd_channels.append(ch)
        source_data['CEDRecordingInterface'].update(smrx_channel_ids=rhd_channels)
        super().__init__(source_data)
