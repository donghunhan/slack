# from django.shortcuts import render
# from django.http import JsonResponse
# from PIL import Image
# import io
# import numpy as np
# import cv2
# import base64
# from ultralytics import YOLO

# # YOLOv8 모델 로드
# model = YOLO(r'C:\Users\dounghun\Desktop\slack\django\best.pt')

# # 색상을 클래스별로 다르게 설정 (랜덤)
# CLASS_COLORS = {}

# def get_class_color(class_id):
#     """클래스 ID에 따라 고유한 색상을 반환"""
#     if class_id not in CLASS_COLORS:
#         CLASS_COLORS[class_id] = tuple(np.random.randint(0, 255, 3).tolist())  # 랜덤 색상
#     return CLASS_COLORS[class_id]

# def detect_and_draw(image):
#     """YOLOv8 감지 후 바운딩 박스 및 클래스명 그리기"""
#     results = model(image)

#     # 원본 이미지 로드
#     image = np.array(image.convert("RGB"))

#     # OpenCV 사용
#     for box, cls, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf):
#         x1, y1, x2, y2 = map(int, box[:4])  # 바운딩 박스 좌표
#         class_id = int(cls)  # 클래스 ID
#         confidence = float(conf)  # 확신도
#         class_name = model.names[class_id]  # 클래스 이름

#         # 클래스별 고유한 색상
#         color = get_class_color(class_id)

#         # 바운딩 박스 그리기
#         cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

#         # 텍스트 넣기 (클래스 이름 + 확신도)
#         label = f"{class_name} ({confidence:.2f})"
#         (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
#         cv2.rectangle(image, (x1, y1 - text_height - 5), (x1 + text_width, y1), color, -1)  # 배경 박스
#         cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     # 결과 이미지를 Base64로 인코딩하여 반환
#     _, encoded_image = cv2.imencode('.jpg', image)
#     encoded_image = base64.b64encode(encoded_image).decode('utf-8')
#     return encoded_image

# def upload_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         # 업로드된 이미지 처리
#         image_file = request.FILES['image']
#         image = Image.open(io.BytesIO(image_file.read()))

#         # YOLO 감지 및 바운딩 박스 그리기
#         result_image = detect_and_draw(image)

#         return JsonResponse({'result_image': result_image})

#     return render(request, 'upload.html')
from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import io
import numpy as np
import cv2
import base64
from ultralytics import YOLO
import tempfile

# YOLOv8 모델 로드
model = YOLO(r'C:\Users\dounghun\Desktop\slack\django\best.pt')

# 색상을 클래스별로 다르게 설정 (랜덤)
CLASS_COLORS = {}

def get_class_color(class_id):
    """클래스 ID에 따라 고유한 색상을 반환"""
    if class_id not in CLASS_COLORS:
        CLASS_COLORS[class_id] = tuple(np.random.randint(0, 255, 3).tolist())  # 랜덤 색상
    return CLASS_COLORS[class_id]

def detect_and_draw(image):
    """YOLOv8 감지 후 바운딩 박스 및 클래스명 그리기"""
    results = model(image)

    # 원본 이미지 로드
    image = np.array(image.convert("RGB"))

    # OpenCV 사용
    for box, cls, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf):
        x1, y1, x2, y2 = map(int, box[:4])  # 바운딩 박스 좌표
        class_id = int(cls)  # 클래스 ID
        confidence = float(conf)  # 확신도
        class_name = model.names[class_id]  # 클래스 이름

        # 클래스별 고유한 색상
        color = get_class_color(class_id)

        # 바운딩 박스 그리기
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # 텍스트 넣기 (클래스 이름 + 확신도)
        label = f"{class_name} ({confidence:.2f})"
        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(image, (x1, y1 - text_height - 5), (x1 + text_width, y1), color, -1)  # 배경 박스
        cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 결과 이미지를 Base64로 인코딩하여 반환
    _, encoded_image = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(encoded_image).decode('utf-8')
    return encoded_image

def detect_video_or_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = file.name.lower()

        # 이미지 파일 처리
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image = Image.open(io.BytesIO(file.read()))
            result_image = detect_and_draw(image)
            return JsonResponse({'result_image': result_image})

        # 동영상 파일 처리
        elif file_name.endswith(('.mp4', '.avi', '.mov')):
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False) as tmp_video:
                tmp_video.write(file.read())
                tmp_video_path = tmp_video.name

            # 동영상 파일 열기
            cap = cv2.VideoCapture(tmp_video_path)
            frames = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # YOLO 객체 감지 후 바운딩 박스 그리기
                pil_frame = Image.fromarray(frame)
                result_image = detect_and_draw(pil_frame)
                frames.append(result_image)

            cap.release()

            # 첫 번째 프레임 결과 반환
            return JsonResponse({'result_image': frames[0]})

        else:
            return JsonResponse({'error': '지원되지 않는 파일 형식입니다.'}, status=400)

    return render(request, 'upload.html')
