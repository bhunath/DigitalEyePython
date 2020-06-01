# DigitalEyePython

python version 3.6

pip install opencv
pip install dlib [pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl]
pip install imutils
pip install flask
pip install numpy
pip install pyqt5
pip install tinydb
python -m pip install plyer


The shape_predictor_68_face_landmarks.dat file is the pre-trained Dlib model for face landmark detection. You can get it from the official Dlib site here: dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2. It's zipped with bz2, so just unzip it to get the .dat file.
White Paper Based on which we are detecting the Eye Liveliness : http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf


Command to Create Installer:
python -m PyInstaller --hidden-import pkg_resources.py2_warn --onefile --add-data "haarcascade_frontalface_default.xml;." --add-data "haarcascade_eye.xml;." --add-data "shape_predictor_68_face_landmarks.dat_2;." --add-data "python.ico;." DigitalEyeApplication.py --name DigitalEye 

