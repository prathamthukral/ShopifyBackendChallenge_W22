from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from PhotoRepoApp.models import Images
from PhotoRepoApp.serializers import ImagesSerializer
from django.core.files.storage import default_storage
from .models import Images
from django.conf import settings
import pymysql
from django.core.files.storage import default_storage
import boto3

# https://guides.lib.umich.edu/c.php?g=282942&p=1885348
image_types = (
    ".tif",
    ".tiff",
    ".bmp",
    ".jpg",
    ".jpeg",
    ".gif",
    ".png",
    ".eps",
    ".raw",
    ".cr2",
    ".nef",
    ".orf",
    ".sr2"
)

# Create your views here.
@csrf_exempt
def imageApi(request,filename="",tag=""):
    if request.method=='GET':
        filename = request.GET.get('filename','')
        tag = request.GET.get('tag','')

        if not filename and not tag:
            images=Images.objects.all()
        if filename:
            images=Images.objects.filter(Filename=filename)
        elif tag:
            images=Images.objects.filter(Tag__contains=tag)
        
        if(len(images)==0):
            return JsonResponse("No results found.",safe=False)

        image_serializer=ImagesSerializer(images,many=True)        
        return JsonResponse(image_serializer.data,safe=False)
    elif request.method=='POST' or request.method=='DELETE':
        image_data=JSONParser().parse(request)

        if not image_data['filename'].endswith(image_types):
            return JsonResponse(f"Failed. Not an approved image file type.",safe=False)        

        pymysql.install_as_MySQLdb()
        db_settings=settings.DATABASES["default"]
        conn=pymysql.connect(
            host=db_settings["HOST"],
            port=int(db_settings["PORT"]),
            user=db_settings["USER"],
            password=db_settings["PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )        

        # upload image to s3 if successful insertion into sql
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        LocalPath = settings.MEDIAFILES_LOCATION+"/"+image_data['filename']
        LocalPath = LocalPath.replace("\\","/")
        S3Path = settings.S3_IMAGE_PATH+"/"+image_data['filename']

        if request.method=='POST':
            # insert record into sql
            query=f"""INSERT INTO `shopify_image_db`.`PhotoRepoApp_images` 
                (`Filename`, `LocalPath`, `S3Path`, `Tag`) 
                VALUES ('{image_data['filename']}', '{LocalPath}', '{S3Path}', '{image_data['tag']}');"""
            
            cursor=conn.cursor()
            try:
                cursor.execute(query)
            except Exception as err:
                return JsonResponse(f"Failed. {err}",safe=False)

            s3_client.upload_file(LocalPath, settings.AWS_STORAGE_BUCKET_NAME, S3Path)
        else:
            query=f"DELETE FROM `shopify_image_db`.`PhotoRepoApp_images` WHERE Filename='{image_data['filename']}'"
            cursor=conn.cursor()
            try:
                cursor.execute(query)
            except Exception as err:
                return JsonResponse(f"Failed. {err}",safe=False)
            
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=S3Path)
        
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse(f"Accepted {request.method} request.",safe=False)