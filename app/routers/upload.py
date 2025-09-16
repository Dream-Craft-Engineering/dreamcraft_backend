import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..deps import get_current_admin # To protect the endpoint
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
    # Define the path to save the image
    save_path = "static/images"
    
    # Generate a unique filename to prevent overwrites
    unique_id = uuid.uuid4().hex
    # Get the file extension (e.g., .jpg, .png)
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{unique_id}.{file_extension}"
    
    file_location = f"{save_path}/{unique_filename}"

    try:
        # Save the file to the specified location
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Return the public URL of the saved file
    return {"file_url": f"/static/images/{unique_filename}"}