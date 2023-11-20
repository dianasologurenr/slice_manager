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

def get_images(db: Session, skip: int = 0, limit: int = 100):
    db_images = db.query(models_image.Image).offset(skip).limit(limit).all()
    images = [convert_sqlalchemy_to_pydantic(db_image) for db_image in db_images]
    return images

def get_image(db: Session, id: int):
    image = db.query(models_image.Image).filter(models_image.Image.id == id).first()
    return convert_sqlalchemy_to_pydantic(image)

def get_image_by_name(db: Session, name: str):
    image = db.query(models_image.Image).filter(models_image.Image.name == name).first()
    return image

def create_image(db: Session, image: schema.ImageBase):
    db_image = models_image.Image(
        name=image.name,
        description=image.description
        )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return convert_sqlalchemy_to_pydantic(db_image)

def update_image(db: Session, id: int, image: schema.ImageUpdate):
    db_image = db.query(models_image.Image).filter(models_image.Image.id == id).first()
    
    image_data = image.dict(exclude_unset=True)

    for key, value in image_data.items():
        setattr(db_image, key, value)

    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return convert_sqlalchemy_to_pydantic(db_image)

    
def delete_image(db: Session, id: int):
    db_image = db.query(models_image.Image).filter(models_image.Image.id == id).first()
    db.delete(db_image)
    db.commit()
    return {"message": "Image deleted successfully"}

def convert_sqlalchemy_to_pydantic(image: models_image.Image) -> schema.Image:
    if image:
        return schema.Image(
            name=image.name,
            description=image.description,
            id=image.id,
            path=image.path,
            status=image.status.value
        )
    return None