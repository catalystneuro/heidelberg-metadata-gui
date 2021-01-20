# from nwb_conversion_tools import NWBConverter, CEDRecordingInterface
# from .heidelberg_ophys_interface import HeidelbergOphysInterface
# from .heidelberg_ecephys_interface import HeidelbergEcephysInterface


# class HeidelbergNWBConverter(NWBConverter):

#     # Modular data interfaces
#     data_interface_classes = {
#         # 'HeidelbergEcephysInterface': HeidelbergEcephysInterface,
#         'CEDRecordingInterface': CEDRecordingInterface,
#         'HeidelbergOphysInterface': HeidelbergOphysInterface,
#     }

#     def __init__(self, source_data):
#         channel_info = CEDRecordingInterface.get_all_channels_info(source_data['CEDRecordingInterface']['file_path'])
#         rhd_channels = []
#         for ch, info in channel_info.items():
#             if "Rhd" in info["title"]:
#                 rhd_channels.append(ch)
#         source_data['CEDRecordingInterface'].update(smrx_channel_ids=rhd_channels)
#         super().__init__(source_data)


from nwb_conversion_tools.utils import get_base_schema, get_schema_from_hdmf_class, get_schema_for_NWBFile
from pynwb import NWBFile
import pynwb
import importlib.resources as pkg_resources
import json

from .utils import get_basic_metadata
from . import schema

class HeidelbergNWBConverter:

    def __init__(self, metadata_schema=None):
        pass

    def get_metadata_schema(self):
        # with pkg_resources.open_text(schema, 'metadata_schema_ecephys.json') as f:
        #     metadata_schema = json.load(f)
        # return metadata_schema
        metadata_schema = get_base_schema(
            id_='metadata.schema.json',
            root=True,
            title='Metadata',
            description='Schema for the metadata',
            version="0.1.0",
            required=["NWBFile"],
            properties=dict(
                NWBFile=get_schema_for_NWBFile(),
                Subject=get_schema_from_hdmf_class(pynwb.file.Subject)
            )
        )
        metadata_schema['properties']['Ecephys'] = get_base_schema(tag='Ecephys')
        metadata_schema['properties']['Ecephys']['properties']['Device'] = get_schema_from_hdmf_class(pynwb.device.Device)
        metadata_schema['properties']['Ecephys']['properties']['ElectrodeGroup'] = get_schema_from_hdmf_class(pynwb.ecephys.ElectrodeGroup)
        metadata_schema['properties']['Ecephys']['properties']['ElectricalSeries_raw'] = get_schema_from_hdmf_class(pynwb.ecephys.ElectricalSeries)
        return metadata_schema

    def get_metadata(self):
        """Auto-fill as much of the metadata as possible."""
        metadata = get_basic_metadata()
        metadata['Ecephys'] = dict(
            Device=dict(name='Device_ecephys'),
            ElectrodeGroup=dict(
                name='ElectrodeGroup',
                description='description',
                location='location',
                device='Device_ecephys'
            ),
            ElectricalSeries_raw=dict(
                name='ElectricalSeries_raw',
                description='ADDME',
                rate=1000.
            )
        )
        return metadata