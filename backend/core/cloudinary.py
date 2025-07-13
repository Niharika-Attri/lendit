import cloudinary
from cloudinary.uploader import upload
from fastapi import APIRouter, UploadFile, HTTPException, status

# Configuration       
cloudinary.config( 
    cloud_name = "djopmrv4e", 
    api_key = "473857625732351", 
    api_secret = "<your_api_secret>", 
    secure=True
)

async def upload_image(image: UploadFile):
    try:
        upload_result = upload(image.file)
        file_url = upload_result['secure_url']
        return file_url
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading images: {e}")
    

async def handle_upload(image: UploadFile):
    try:
        url = await upload_image(image)
        return url
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
