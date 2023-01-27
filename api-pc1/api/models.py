import os, base64, io
from PIL import Image
import datetime
from datetime import datetime
from sqlalchemy import create_engine

# Guardar la imagen en la carpeta, utilizando un volumen de docker en el path de esta carpeta
def guardar_imagen(imagen_name, imagen_data):
    #if not os.path.exists(upload_folder):
    #    os.makedirs(upload_folder)    
    upload_folder = '/app/data/'
    image = base64.b64encode(str.encode(imagen_data))       
    fileName = imagen_name + next_nro(upload_folder + "/" + imagen_name)

    imagePath = (upload_folder+fileName)
    img = Image.open(io.BytesIO(image))
    img.save(imagePath, 'jpg')
        

# Genera nombre de imagen
def next_nro(path):
    i = 1
    while os.path.exists(path + str(i)):
        i += 1
    return str(i)

######### Data Base ##################

# conexión mysql
def conexion_mysql():
    engine = create_engine("mysql+pymysql://mbit:mbit@localhost:3306/Pictures")
    return engine

# Insertar en tabla de pictures y tags
def insertar_pictures(engine, path_img, tags, confidence):
    #fecha = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))

    fecha = str(datetime.now())
    with engine.connect() as conn:
        conn.execute(f"INSERT INTO pictures VALUES (0, '{path_img}','{fecha}')")

        id = get_pictureId(conn)
        picture_id = id[0]['id']

        for (tag) in tags:
            conn.execute(f"INSERT INTO tags VALUES ('{tag}','{picture_id}',{confidence},'{fecha}')")

# Get last picture id
def get_pictureId(conn):
    result = conn.execute("SELECT max(id) as id FROM pictures")
    columns = result.keys()
    data = [
            dict(zip(columns, row))
            for row in result
            ]
    return data

####################################
# Insertar en tabla de tags
#def insertar_tags(engine, tags, confidence):
#    with engine.connect() as conn:
#        id = get_pictureId(conn)
#        picture_id = id[0]['id']

#        for (tag) in tags:
#            conn.execute(f"INSERT INTO tags VALUES ('{tag}','{picture_id}',{confidence},'{str(datetime.strptime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S'))}')")



################## QUERYS ##################

#Obtener tags de la BDD
def get_tags(conn, min_date, max_date):
    if min_date =="":
        min_date = datetime.datetime.min
    
    if max_date =="":
        max_date = datetime.datetime.max

    result = conn.execute("SELECT picture_id, tag, confidence FROM tags WHERE cast(date as date) >= cast('" + min_date + "' as date) and cast(date as date) <= cast('" + max_date + "' as date) ")
    columns = result.keys()
    data = [
            dict(zip(columns, row))
            for row in result
            ]

    return data
