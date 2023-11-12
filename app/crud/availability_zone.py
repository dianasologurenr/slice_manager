from sqlalchemy.orm import Session

from models import user as models_user
from models import slice_user as models_slice_user
from models import slice as models_slice
from models import availability_zone as models_availability_zone
from models import node as models_node
from models import server as models_server
from models import image as models_image
from models import flavor as models_flavor
from models import security as models_security
from models import port as models_port
from models import link as models_link
from models import monitoreo as models_monitoreo
from models import inbound as models_inbound
from models import outbound as models_outbound
from models import alerts as models_alerts
from schemas import schema

def get_availability_zone(db: Session, skip: int = 0, limit: int = 100):
    db_availability_zones = db.query(models_availability_zone.AvailabilityZone).offset(skip).limit(limit).all()
    availability_zones = [convert_sqlalchemy_user_to_pydantic(db_availability_zone) for db_availability_zone in db_availability_zones]
    return availability_zones


def convert_sqlalchemy_user_to_pydantic(availability_zone: models_availability_zone.AvailabilityZone) -> schema.User:
    return schema.AvailabilityZone(
        id = availability_zone.id,
        name = availability_zone.name,
        latitude = availability_zone.latitude,
        longitude = availability_zone.longitude
    )


