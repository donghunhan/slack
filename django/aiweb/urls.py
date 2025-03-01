from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 기본 인덱스 페이지
    path('upload/', views.detect_video_or_image, name='upload_file'),  # 이미지와 동영상을 처리하는 하나의 엔드포인트
    path('debug/', views.debug_view, name='debug'),  # 디버깅용 단순 페이지
]