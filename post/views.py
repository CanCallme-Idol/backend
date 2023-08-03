from django.shortcuts import render, redirect
from rest_framework import generics
from star.staroasis import base_model
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from rest_framework import serializers


class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

class ImgProcSerializer(serializers.ModelSerializer):
	
    def img_resize(img: InMemoryUploadedFile) -> InMemoryUploadedFile:
        pil_img = Image.open(img).convert('RGBA')
        pil_img = pil_img.resize((1000,1000))

        new_img_io = BytesIO()
        pil_img.save(new_img_io, format='PNG')
        result = InMemoryUploadedFile(
            new_img_io, 'ImageField', img.name, 'image/png', new_img_io.getbuffer().nbytes, img.charset
        )
        return result
    
    
    
@api_view(['POST'])
def face_service(request):
    if request.method == 'POST':
        
        img = request.FILES.get('file')
        
        img_path = default_storage.save('./star/userface/' + img.name, img)
        print(img_path)
        print(img.name)
        
        try:
            t,p,i = base_model(img_path)
        except Exception as e:
            result = {
                'errorMessage' : e.args,
            }
            print("오류내용 : ",e.args)
            return Response(result)
        
        print(f'당신이 {t}상일 확률은 {p}입니다!')
        print(f'특히 {i} 아티스트를 가장 닮았습니다')
        
        result = {
            'company' : t,
            'percentage' : p,
            'lookslike' : i
        }
    
    return Response(result)


@api_view(['POST'])
def apitest(request):
    if request.method == 'POST':
        return Response("연결 됨~~~connect~!~!")




# img = request.FILES
        # pil_img = Image.open(img).convert('RGBA')
        # pil_img = pil_img.resize((1000,1000))
        # print(pil_img, type(pil_img))
        # # print(img, type(img))
        # new_img_io = BytesIO()
        # # pil_img.save(os.getcwd() + pil_img, format='PNG')
        # pil_img.save(new_img_io, format='PNG')
        
        # result = InMemoryUploadedFile(
        #     new_img_io, 'ImageField', img.name, 'image/png', new_img_io.getbuffer().nbytes, img.charset
        # )
        # print(result)
        # # img_path = default_storage.save('star/' + pil_img)
        # # img_path
        