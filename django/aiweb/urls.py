from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.detect_video_or_image, name='upload_file'),  # 이미지와 동영상을 처리하는 하나의 엔드포인트
]