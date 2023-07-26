from django.shortcuts import render
from rest_framework import generics
from .star.staroasis import base_model
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['POST'])
def face_service(request):
    if request.method == 'POST':
        img = request.FILES.get("img")
        
        t,p,i = base_model(img)
        print(f'당신이 {t}상일 확률은 {p}입니다!')
        print(f'특히 {i} 아티스트를 가장 닮았습니다')
    
    return render(request, '')