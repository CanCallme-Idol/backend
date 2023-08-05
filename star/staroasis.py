from deepface import DeepFace
import numpy as np
import cv2
from mtcnn import MTCNN
from random import randrange
import os
def avg_score(score,num):
  if len(score)>=num:
    return sum(score[:num])/num
  else:
    return sum(score)/len(score)

def softmax(x):
    epsilon = 1e-5  
    f_x = np.exp(x) / (np.sum(np.exp(x)) + epsilon)
    return f_x
def valid_face(path):
  detector = MTCNN()
  # Read the input image
  image =  cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
  name = path.split('.')[0]
  tmp_path = f'{randrange(10000)}_tmp.jpg'
  try:
    if image.shape[-1]>3:
          image = cv2.cvtColor(image,cv2.COLOR_RGBA2RGB)
    # Detect faces in the image
    faces = detector.detect_faces(image)
    faces
  except:
    raise Exception('이미지 경로를 확인해주세요.')
  if len(faces)==1:
    result = cv2.imwrite(tmp_path, image)
    if result:
      return tmp_path
    else:
      raise Exception('Valid_face후에 이미지가 저장되지 않았습니다.')
  elif len(faces)>1:
    raise Exception('두명의 이미지는 분석이 불가능합니다.')
  else:
    raise Exception('얼굴이 검출되지 않았습니다.')

def base_model(image):
  path = valid_face(image)
  hybe = DeepFace.find(img_path = path,    # the image to compare against
              db_path = "hybe",    # folder containing all the images
              model_name = 'ArcFace',
              enforce_detection = False)[0]

  sm = DeepFace.find(img_path = path,    # the image to compare against
                db_path = "sm",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]

  jyp = DeepFace.find(img_path = path,    # the image to compare against
                db_path = "jyp",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]

  yg = DeepFace.find(img_path = path,    # the image to compare against
                db_path = "yg",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]
  
  lst = ['jyp','hybe','yg','sm']
  data = [-avg_score(jyp['ArcFace_cosine'],5),-avg_score(hybe['ArcFace_cosine'],5),-avg_score(yg['ArcFace_cosine'],5),-avg_score(sm['ArcFace_cosine'],5)]
  target = lst[np.argmax(data)]
  probabilities = softmax(data)[np.argmax(data)] + (softmax(data)[np.argmax(data)]-0.25)*10
  identity = eval(target)['identity'][0].split('/')[-1].split('_')[0]
  os.remove(path)
  return target, probabilities,identity

if __name__ == '__main__':
    t, p,i = base_model('한글.jpeg')
    print(f'당신이 {t}상일 확률은 {p}입니다!')
    print(f'특히 {i} 아티스트를 가장 닮았습니다')
