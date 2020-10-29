from nwb_conversion_tools.basedatainterface import BaseDataInterface
from nwb_conversion_tools.utils import get_metadata_schema, get_base_schema, get_schema_from_hdmf_class
from pynwb import NWBFile
import pynwb
import importlib.resources as pkg_resources
import json

from .utils import get_basic_metadata
from . import schema


class HeidelbergEcephysInterface(BaseDataInterface):

    @classmethod
    def get_input_schema(cls):
        with pkg_resources.open_text(schema, 'input_schema_ecephys.json') as f:
            input_schema = json.load(f)
        return input_schema

    def __init__(self, **input_args):
        super().__init__(**input_args)

    def get_metadata_schema(self):
        metadata_schema = get_metadata_schema()
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

    def convert_data(self, nwbfile: NWBFile, metadata_dict: dict,
                     stub_test: bool = False):
        raise NotImplementedError('Conversion not implemented')
