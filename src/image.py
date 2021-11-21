
# from PIL import Image
# from io import BytesIO
# from numpy import array, asarray
# import matplotlib.pyplot as plt

# # image = Image.open('C:/Users/ASUS/Desktop/b.jpg')
# # image = image.resize([1000, 1000])
# # print(asarray(image).shape)
# # print(asarray(image).flatten(order='C'))
# # plt.imshow(image)
# # plt.show()

# from skimage.io import imread
# from skimage.util import crop
# import matplotlib.pyplot as plt

# img = imread('C:/Users/ASUS/Desktop/Dataset_arañas/araña_bananera/9600033.jpg')
# plt.imshow(img)
# plt.show()
# print(img.flatten(order='C').shape)
# img = (img/127)-1
# print(img.flatten(order='C').shape)
# plt.imshow(img)
# plt.show()
# # a = img.shape[0]-1000
# # b = img.shape[1]-1000
# # img = crop(img, ((int(a/2), int(a/2)), (int(b/2), int(b/2)), (0, 0)), copy=False)
# # print(img.shape)
# # plt.imshow(img)
# # plt.show()

import os


print(os.path.basename(os.path.splitext('E:/WORLD/PYTHOM/AraneaeIA/src/data/Araneae.xlsx')[1]))