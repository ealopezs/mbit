from imagekitio import ImageKit
import base64
import json

def set_imagekit():
   with open('credentials.json', 'r') as f:
        config = json.load(f)
        public_key_config=config["ImageKit"]["public_key"]
        private_key_config=config["ImageKit"]["private_key"]
        
        imagekit = ImageKit(
            public_key = public_key_config,
            private_key = private_key_config,
            url_endpoint = 'https://ik.imagekit.io/elio/'
            )
        return imagekit

#upload imagen
def subir_imagen(imagen):
        imagekit = set_imagekit()
        with open(imagen, mode="rb") as img:
            imgstr = base64.b64encode(img.read())
        
        # upload an image
        upload_info = imagekit.upload(file=imgstr, file_name="img")
     
        return upload_info

# eliminar imagen
def delete_image(file_id):
    imagekit = set_imagekit()
    delete = imagekit.delete_file(file_id=file_id)