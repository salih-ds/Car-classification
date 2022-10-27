import os
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import PIL
from PIL import ImageOps, ImageFilter
import random


class DataInfo:
 
  def __init__(self, class_names, path):
    self.class_names = class_names  # список названий классов в соответствии разметкой датасета (list)
    self.path = path  # путь к датасету (str)

  # распределение по классам
  def class_distribution(self):
    print('Распределение по классам:')
    for num, i in enumerate(self.class_names):
      train_path_all = f'{self.path}{num}/'
      num_files = len([f for f in os.listdir(train_path_all)
                    if os.path.isfile(os.path.join(train_path_all, f))])
      print(f'{i}:  {num_files}')



  # пример изображений по классам
  def view_class_image(self):
    # посмотрим на картинки
    print('Пример картинок')
    plt.figure(figsize=(16,8))

    for num, i in enumerate(self.class_names):
      train_path_all = f'{self.path}{num}/'
      rand_files = random.choice(os.listdir(train_path_all))
      im = PIL.Image.open(f'{train_path_all}/{rand_files}')
      plt.subplot(3,4, num+1)
      plt.imshow(im)
      plt.title('Class: '+str(i))
      plt.axis('off')
    plt.show()



  # средний размер изображений
  def mean_size_img(self):
    sum_width = 0
    sum_height = 0
    counter = 0

    for num, i in enumerate(self.class_names):
      train_path_all = f'{self.path}{num}/'

      # max_width = 0
      # max_height = 0
      for z in os.listdir(train_path_all):
          im = PIL.Image.open(f"{train_path_all}{z}")
          sum_width += im.size[0]
          sum_height += im.size[1]
          counter += 1
      
    mean_width = sum_width/counter
    mean_height = sum_height/counter

    print(f'mean_width:{mean_width}   mean_height:{mean_height}   for {counter} images')
