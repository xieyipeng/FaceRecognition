import numpy as np
from PIL import Image
import os
import time
from tools.vgg.transforms import *
from skimage import io
from skimage.transform import resize
from tools.vgg.models import *

t1 = time.time()

cut_size = 44

transform_test = transforms.Compose([
    transforms.TenCrop(cut_size),
    transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
])


def emotion(frame=None, face_path='images/face.jpg'):
    if frame is None:
        raw_img = io.imread(face_path)
    else:
        raw_img = frame
    gray = rgb2gray(raw_img)
    gray = resize(gray, (48, 48), mode='symmetric').astype(np.uint8)
    img = gray[:, :, np.newaxis]
    img = np.concatenate((img, img, img), axis=2)
    img = Image.fromarray(img)
    inputs = transform_test(img)

    class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    net = VGG('VGG19')
    # checkpoint = torch.load(os.path.join('FER2013_VGG19', 'PrivateTest_model.t7'))
    checkpoint = torch.load(os.path.join('/home/xieyipeng/code/Graduation-Design/combine/model/CK+_VGG19/10/Test_model.t7'))
    net.load_state_dict(checkpoint['net'])
    net.cuda()
    net.eval()

    n_crops, c, h, w = np.shape(inputs)

    inputs = inputs.view(-1, c, h, w)
    inputs = inputs.cuda()
    inputs = Variable(inputs, volatile=True)
    outputs = net(inputs)

    outputs_avg = outputs.view(n_crops, -1).mean(0)  # avg over crops

    score = F.softmax(outputs_avg)
    _, predicted = torch.max(outputs_avg.data, 0)

    # return class_names[predicted.item()], score[predicted.item()].item()
    return class_names[predicted.item()], score


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


if __name__ == '__main__':
    print(emotion(face_path='images/S026_006_00000013.png'))
