from . import models
from . import imagekit_up
from . import imagga_tag

#Subir y "taggear" imagen
def tags_image(b64str_image, min_confidence):

    #1. Usamos imagekit.io para subir la imagen a la nube de forma pública.
    upload_image=imagekit_up.subir_imagen(b64str_image)

    #2. Usamos https://imagga.com/ para extraer tags a partir de la imagen subida anteriormente.
    tags = imagga_tag.extraer_tags(min_confidence, upload_image.url)
    
    #3. Borramos la imagen subida a https://docs.imagekit.io/ usando la api delete.
    imagekit_up.delete_image(upload_image.file_id)

    #4. Almacena en la carpeta (volumen) del docker
    #models.guardar_imagen("imagen_", b64str_image)

    #5. Almacenamos información en la base de datos
    engine = models.conexion_mysql()
    #if res:
    models.insertar_pictures(engine, upload_image.url, tags, min_confidence)

    #models.insertar_tags(engine, tags, min_confidence)    
    #else:
    #    raise Exception(msg)

    return tags

#end point consulta de imágenes y tagas
def get_tags_db(min_date, max_date):
    engine = models.conexion_mysql()
    data = models.get_tags(engine, min_date, max_date)

    return data