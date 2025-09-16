import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..deps import get_current_admin 
from .. import models

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/image/")
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_admin)
):
    """
    Uploads an image, saves it, and returns the public URL.
    """
    
    save_path = "static/images"
    
   
    unique_id = uuid.uuid4().hex
    
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{unique_id}.{file_extension}"
    
    file_location = f"{save_path}/{unique_filename}"

    try:
        
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

   
    return {"file_url": f"/static/images/{unique_filename}"}