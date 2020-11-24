from nwb_conversion_tools.basedatainterface import BaseDataInterface
from nwb_conversion_tools.utils import get_base_schema, get_schema_from_hdmf_class
from pynwb import NWBFile
import pynwb
import importlib.resources as pkg_resources
import json

from .utils import get_basic_metadata
from . import schema


class HeidelbergOphysInterface(BaseDataInterface):

    @classmethod
    def get_source_schema(cls):
        with pkg_resources.open_text(schema, 'source_schema_ophys.json') as f:
            source_schema = json.load(f)
        return source_schema

    def __init__(self, **source_data):
        super().__init__(**source_data)

    def get_metadata_schema(self):
        metadata_schema = super().get_metadata_schema()
        metadata_schema['properties']['Ophys'] = get_base_schema(tag='Ophys')
        metadata_schema['properties']['Ophys']['properties']['Device'] = get_schema_from_hdmf_class(pynwb.device.Device)

        return metadata_schema

    def get_metadata(self):
        """Auto-fill as much of the metadata as possible."""
        metadata = get_basic_metadata()
        metadata['Ophys'] = dict(
            Device=dict(name='Device_ophys'),
        )
        return metadata

    def convert_data(self, nwbfile: NWBFile, metadata_dict: dict,
                     stub_test: bool = False):
        raise NotImplementedError('Conversion not implemented')
