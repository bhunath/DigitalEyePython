import urllib.request

print('Beginning file download with urllib2...')

url = 'https://github.com/bhunath/DigitalEyePython/blob/master/shape_predictor_68_face_landmarks.dat_2?raw=true'
urllib.request.urlretrieve(url, 'shape_predictor_68_face_landmarks.dat_2_2')