import os
import shutil
from dependencies import get_db
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from crud import images as crud_image
import schemas.schema as schema
from typing import List, Optional

ALLOWED_EXTENSIONS = {'.iso', '.vmdk', '.vhd', '.vhdx', '.qcow2', '.img'}
IMAGE_FOLDER = "image_folder"

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Image])
async def read_images(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    images = crud_image.get_images(db, skip=skip, limit=limit)
    return images

@router.get("/{id}",response_model=schema.Image)
async def read_image(id: int, db=Depends(get_db)):
    db_image = crud_image.get_image(db, id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.post("/", response_model=schema.Image)
async def create_image(name: str = Form(...),
                       description: Optional[str] = Form(None),
                       image_file: UploadFile = File(...),
                       db=Depends(get_db)):

    db_image = crud_image.get_image_by_name(db,name=name)
    if db_image:
        raise HTTPException(status_code=400, detail="Name already registered")
    if not allowed_file(image_file.filename):
        raise HTTPException(status_code=400, detail="Archivo no permitido")

    # Creating image
    new_image = crud_image.create_image(
        db=db, 
        image=schema.ImageBase(
            name=name, description=description))
    
    # Saving file
    image_folder = get_image_storage_folder()
    file_location = os.path.join(image_folder, f"{new_image.id}_{image_file.filename}")

    if os.path.exists(file_location):
        raise HTTPException(status_code=400, detail="File already exists")

    try:
        with open(file_location, "wb") as file:
            shutil.copyfileobj(image_file.file, file)
        return crud_image.update_image(db=db, 
                                       id=new_image.id, 
                                       image=schema.ImageUpdate(status="disponible",path=file_location))
    except:
        crud_image.update_image(db=db, 
                                id=new_image.id, 
                                image=schema.ImageUpdate(status="error"))
        raise HTTPException(status_code=404, detail="Image couldn't be uploaded")


# # Image update if needed
# @router.patch("/{id}", response_model=schema.Image)
# def update_image(id: int, image: schema.ImageUpdate,db=Depends(get_db)):
#     db_image = crud_image.get_image(db=db, id=id)
    
#     if not db_image:
#         raise HTTPException(status_code=404, detail="Image not found")
    
#     return crud_image.update_image(db=db,id=id,image=image)
    

@router.delete("/{id}")
async def delete_image(id: str,db=Depends(get_db)):
    db_image = crud_image.get_image(db, id=id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    
    if delete_file(db_image.path):
        return crud_image.delete_image(db=db, id=id)
    else:
        raise HTTPException(status_code=404, detail="Image couldn't be deleted")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_storage_folder():
    current_dir = os.getcwd()
    target_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    image_storage_path = os.path.join(target_dir, IMAGE_FOLDER)
    if not os.path.exists(image_storage_path):
        os.makedirs(image_storage_path)
    return image_storage_path

def delete_file(filepath):
    # Verificar si el archivo existe
    if os.path.exists(filepath):
        # Eliminar el archivo
        os.remove(filepath)
        return True
    else:
        return False