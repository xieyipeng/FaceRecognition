import os
import keras
from keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from keras.optimizers import SGD
from models import simple_CNN
from utils import load_data, preprocess_input
import keras.backend as K

"""
import tensorflow.compat.v1 as tf

init = tf.global_variables_initializer()
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

tf.keras.backend.set_session(session)
keras.backend.clear_session()  # 此句代码分量很重

session.run(init)
"""

data_path = '/home/xieyipeng/code/dataset/FER2013/fer2013/fer2013.csv'
model_save_path = 'trained_models/simpler_CNN.{epoch:02d}-{val_accuracy:.2f}.hdf5'

# 加载人脸表情训练数据和对应表情标签
faces, emotions = load_data(data_path)

# 人脸数据归一化，将像素值从0-255映射到0-1之间
faces = preprocess_input(faces)
# 得到表情分类个数
num_classes = emotions.shape[1]

# (48, 48, 1)
image_size = faces.shape[1:]

batch_size = 128
num_epochs = 100

model = simple_CNN(image_size, num_classes)

# 断点续训
if os.path.exists(model_save_path):
    model.load_weights(model_save_path)
    # 若成功加载前面保存的参数，输出下列信息
    print("checkpoint_loaded")

# 编译模型，categorical_crossentropy多分类选用
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 记录日志
csv_logger = CSVLogger('training.log')

# 保存检查点
model_checkpoint = ModelCheckpoint(model_save_path,
                                   monitor='val_acc',
                                   verbose=1,
                                   save_best_only=False)

model_callbacks = [model_checkpoint, csv_logger]

# 训练模型
model.fit(faces, emotions, batch_size, num_epochs,
          verbose=1,
          callbacks=model_callbacks,
          validation_split=.1,
          shuffle=True)
