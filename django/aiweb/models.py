from django.db import models

# Create your models here #디비에저장

class DetectionResult(models.Model):
    image = models.ImageField(upload_to='uploads/')  # 업로드된 원본 이미지
    detected_image = models.ImageField(upload_to='detections/', null=True, blank=True)  # 바운딩 박스가 그려진 이미지
    object_name = models.CharField(max_length=100)  # 감지된 객체 이름
    confidence = models.FloatField()  # 확신도(신뢰도)
    x1 = models.IntegerField()
    y1 = models.IntegerField()
    x2 = models.IntegerField()
    y2 = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # 감지 시간