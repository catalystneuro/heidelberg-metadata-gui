from nwb_conversion_tools import NWBConverter

from .heidelberg_ophys_interface import HeidelbergOphysInterface
from .heidelberg_ecephys_interface import HeidelbergEcephysInterface


class HeidelbergNWBConverter(NWBConverter):

    # Modular data interfaces
    data_interface_classes = {
        'HeidelbergEcephysInterface': HeidelbergEcephysInterface,
        'HeidelbergOphysInterface': HeidelbergOphysInterface,
    }

    def __init__(self, source_data):
        super().__init__(source_data)
