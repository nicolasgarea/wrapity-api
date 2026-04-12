from app.core.exceptions import CloudinaryUploadException
import cloudinary
import cloudinary.uploader

config = cloudinary.config(secure=True)


cloudinary.config(secure=True)


class CloudinaryClient:
    def upload_avatar(self, file: bytes, public_id: str) -> str:
        try:
            result = cloudinary.uploader.upload(
                file,
                public_id=public_id,
                folder="avatars",
                overwrite=True,
                resource_type="image",
            )
            return result["secure_url"]
        except Exception as e:
            raise CloudinaryUploadException() from e
