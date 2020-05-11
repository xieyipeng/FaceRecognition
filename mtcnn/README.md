TensorFlow训练MTCNN记录
参考项目地址github
感谢这位同学，感谢这位同学，感谢这位同学，重要的事情说三遍
MTCNN网络是分为P-Net、R-Net和O-Net三个部分，所以它和一般网络不同的地方是数据准备和训练过程是交叉的。

训练过程
Step 1 下载Wider Face 数据集
可以从官方网站下载Wider Face Training部分并解压缩替换WIDER_train这个文件夹。
因为接下来生成生成negative、positives and part faces的时候，图片数量会变的更炒鸡巨大，所以可以只用一小部分数据试一下，我上传到了百度云，是原始数据的其中两个小的文件夹，提取码kuqw。

Step 2 生成P-Net的训练数据
运行 gen_shuffle_data.py，参数设置为12，生成P-Net的训练数据
运行 gen_tfdata_12net.py，生成对应的 tfrecords 数据格式文件

Step 3 训练P-Net
运行 mtcnn_pnet_test.py，训练P-Net

Step 4 生成R-Net的训练数据
运行 tf_gen_12net_hard_example.py和gen_shuffle_data.py （参数设置为24）
运行 gen_tfdata_24net.py，合并数据并生成对应的 tfrecords 数据格式文件

Step 5 训练R-Net
运行mtcnn_rnet_test.py，训练R-Net

Step 6 生成O-Net的训练数据
运行 gen_24net_hard_example.py 和 gen_shuffle_data.py （参数设置为48）
运行 gen_tfdata_48net.py，合并数据并生成对应的 tfrecords 数据格式文件

Step 7 训练O-Net
运行mtcnn_onet_test.py，训练O-Net

Step 8 测试
运行 test_img.py，参数接你的图片路径和模型路径

说明
1.其中PNet在训练阶段的输入尺寸为12乘12,RNet的输入尺寸为24乘24, ONet的输入尺寸为48乘48.
2.P-Net、R-Net、O-Net分别训练，先训练P-Net，R-Net根据训练的P-Net生成hard样本再训练，O-Net同理。
3.以上的训练过程中生成的hard样本依然是根据原作者的模型，如果使用自己训练的模型，记得修改参数路径

def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--pnet_model', type=str,
                        help='The path of pnet model to generate hard example',
                        default='../save_model/seperate_net/pnet/pnet-3000000')
    
    return parser.parse_args(argv)
1
2
3
4
5
6
7
8
9
4.生成negative:
每张图片会生成50个 negative samples
随机大小，随机位置的裁剪一个小方块称为crop _box，如果crop_box与所有boxes的Iou都小于0.3，那么认为它是nagative sample
生成positives and part faces:
(忽略较小的box)每个box随机生成50个box，在box上进行随机偏移，Iou>=0.65的作为positive examples，0.4<=Iou<0.65的作为part faces，其他忽略
所以图片数量会变的更炒鸡巨大。

最后附上训练过程图片

因为用到的各种预训练模型都是原作者的，数据收敛还是很正常的。
————————————————
版权声明：本文为CSDN博主「上天夭」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_38952721/article/details/94737907