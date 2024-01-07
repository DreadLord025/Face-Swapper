import cv2
import dlib
import numpy as np
import sys
from PIL import Image
import base64
from io import BytesIO

# Инициализация детектора лиц dlib
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

def swap_faces():

    img1 = cv2.imread(sys.argv[1])
    img2 = cv2.imread(sys.argv[2])

    # Обнаружение лиц на изображениях
    faces1 = detector(img1, 1)
    faces2 = detector(img2, 1)

    def process_face(face, img_copy):
        # Выделение лица из изображения
        img_face = img_copy[face.top():face.bottom(), face.left():face.right()]
        img_face = cv2.GaussianBlur(img_face, (5, 5), 0)
        img_face = cv2.getRectSubPix(img_face, (face.right()-face.left(), face.bottom()-face.top()), (img_face.shape[1]/2, img_face.shape[0]/2))

        # Создание маски овала
        mask = np.zeros_like(img_face)
        rows, cols, _ = mask.shape
        mask = cv2.ellipse(mask, center=(rows//2, cols//2), axes=((rows//3) + 20, (cols//2) + 20), angle=0, startAngle=0, endAngle=360, color=(255,255,255), thickness=-1)

        # Применение маски к изображению лица
        img_face = np.bitwise_and(img_face, mask)

        # Добавление альфа-канала для прозрачности черного фона
        b,g,r = cv2.split(img_face)
        alpha = np.where((b==0) & (g==0) & (r==0), 0, 255).astype('uint8')
        img_face = cv2.merge((b,g,r,alpha))

        return img_face

    # Создание копий изображений
    img1_copy = img1.copy()
    img2_copy = img2.copy()

    # Создание экземпляров изображений
    img1_copy_pil = Image.fromarray(cv2.cvtColor(img1_copy, cv2.COLOR_BGR2RGBA))
    img2_copy_pil = Image.fromarray(cv2.cvtColor(img2_copy, cv2.COLOR_BGR2RGBA))

    # Обработка лиц
    if len(faces1) > 0 and len(faces2) > 0:
        # Извлечение прямоугольников, охватывающих лица
        rect1 = faces1[0]
        rect2 = faces2[0]

        # Извлечение координат границ лица
        left1, top1, right1, bottom1 = rect1.left(), rect1.top(), rect1.right(), rect1.bottom()
        left2, top2, right2, bottom2 = rect2.left(), rect2.top(), rect2.right(), rect2.bottom()

        # Вычисление центра лица
        center1_x = (left1 + right1) // 2
        center1_y = (top1 + bottom1) // 2
        center2_x = (left2 + right2) // 2
        center2_y = (top2 + bottom2) // 2

        # Изменение границ лица для более строгого обнаружения
        face1_width = right1 - left1
        face1_height = bottom1 - top1
        left1 = max(0, center1_x - face1_width // 2)
        top1 = max(0, center1_y - face1_height // 2)
        right1 = min(img1.shape[1], center1_x + face1_width // 2)
        bottom1 = min(img1.shape[0], center1_y + face1_height // 2)

        face2_width = right2 - left2
        face2_height = bottom2 - top2
        left2 = max(0, center2_x - face2_width // 2)
        top2 = max(0, center2_y - face2_height // 2)
        right2 = min(img2.shape[1], center2_x + face2_width // 2)
        bottom2 = min(img2.shape[0], center2_y + face2_height // 2)

        # Расширение границ лица
        expand_width = face1_width // 12
        expand_height = face1_height // 12
        left1 = max(0, left1 - expand_width)
        top1 = max(0, top1 - expand_height)
        right1 = min(img1.shape[1], right1 + expand_width)
        bottom1 = min(img1.shape[0], bottom1 + expand_height)

        expand_width = face2_width // 12
        expand_height = face2_height // 12
        left2 = max(0, left2 - expand_width)
        top2 = max(0, top2 - expand_height)
        right2 = min(img2.shape[1], right2 + expand_width)
        bottom2 = min(img2.shape[0], bottom2 + expand_height)

        # Обновление лицевых областей
        faces1[0] = dlib.rectangle(left1, top1, right1, bottom1)
        faces2[0] = dlib.rectangle(left2, top2, right2, bottom2)

        img1_face = process_face(faces1[0], img1_copy)
        img2_face = process_face(faces2[0], img2_copy)

        # Изменение размера изображений лиц
        img1_face = cv2.resize(img1_face, (faces2[0].right()-faces2[0].left(), faces2[0].bottom()-faces2[0].top()))
        img2_face = cv2.resize(img2_face, (faces1[0].right()-faces1[0].left(), faces1[0].bottom()-faces1[0].top()))

        img1_face_pil = Image.fromarray(cv2.cvtColor(img1_face, cv2.COLOR_BGRA2RGBA))
        img2_face_pil = Image.fromarray(cv2.cvtColor(img2_face, cv2.COLOR_BGRA2RGBA))

        # Наложение изображения лица на копию
        img1_copy_pil.paste(img2_face_pil, (faces1[0].left(), faces1[0].top()), img2_face_pil)
        img2_copy_pil.paste(img1_face_pil, (faces2[0].left(), faces2[0].top()), img1_face_pil)

    # Преобразование изображений в строки base64
    img1_bytes = BytesIO()
    img1_copy_pil.save(img1_bytes, format='PNG')
    img1_base64 = base64.b64encode(img1_bytes.getvalue()).decode('utf-8')

    img2_bytes = BytesIO()
    img2_copy_pil.save(img2_bytes, format='PNG')
    img2_base64 = base64.b64encode(img2_bytes.getvalue()).decode('utf-8')

    print(img1_base64)
    print(img2_base64)

swap_faces()