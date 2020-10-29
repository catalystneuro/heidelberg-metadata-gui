from datetime import datetime
import uuid


def get_basic_metadata():
    """Get basic metadata"""

    metadata = dict(
        NWBFile=dict(
            session_description='session description',
            identifier=str(uuid.uuid4()),
            session_start_time=datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        )
    )

    return metadata
