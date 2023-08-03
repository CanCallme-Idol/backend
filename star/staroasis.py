from deepface import DeepFace
import numpy as np
import cv2

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
  # Load the cascade
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
  # Read the input image
  img = cv2.imread(path)
  # Convert into grayscale
  gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  # Detect faces
  faces = face_cascade.detectMultiScale(gray, 1.1, 20)
  if len(faces)==0:
    raise Exception('face not detected. Please use another image!')
  if len(faces)>1:
    raise Exception('Only one faces will be accepted. Please use another image!')
  
def base_model(image):
  valid_face(image)
  hybe = DeepFace.find(img_path = image,    # the image to compare against
              db_path = "star/hybe",    # folder containing all the images
              model_name = 'ArcFace',
              enforce_detection = False)[0]

  sm = DeepFace.find(img_path = image,    # the image to compare against
                db_path = "star/sm",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]

  jyp = DeepFace.find(img_path = image,    # the image to compare against
                db_path = "star/jyp",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]

  yg = DeepFace.find(img_path = image,    # the image to compare against
                db_path = "star/yg",    # folder containing all the images
                model_name = 'ArcFace',
                enforce_detection = False)[0]
  
  lst = ['jyp','hybe','yg','sm']
  data = [-avg_score(jyp['ArcFace_cosine'],5),-avg_score(hybe['ArcFace_cosine'],5),-avg_score(yg['ArcFace_cosine'],5),-avg_score(sm['ArcFace_cosine'],5)]
  target = lst[np.argmax(data)]
  probabilities = softmax(data)[np.argmax(data)]
  identity = eval(target)['identity'][0].split('/')[-1].split('_')[0]
  return target, probabilities,identity

if __name__ == '__main__':
    t, p,i = base_model('jyp/sohi2.jpg')
    print(f'당신이 {t}상일 확률은 {p}입니다!')
    print(f'특히 {i} 아티스트를 가장 닮았습니다')
