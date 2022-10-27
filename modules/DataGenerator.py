from tensorflow.keras.preprocessing.image import ImageDataGenerator
import itertools
import numpy as np, pandas as pd, matplotlib.pyplot as plt


# просмотр сгенерированных изображений
def view_generation_images(generator, count=8, labels=True, figsize=(26, 8), normalized=False):
    # generator - генератор класса DataGenerator

    generator = itertools.islice(generator, count)
    fig, axes = plt.subplots(nrows=1, ncols=count, figsize=figsize)
    for batch, ax in zip(generator, axes):
        if labels:
            img_batch, labels_batch = batch
            img, label = img_batch[0], np.argmax(labels_batch[0]) # берем по одному изображению из каждого батча
        else:
            img_batch = batch
            img = img_batch[0]
        if not normalized:
            img = img.astype(np.uint8)
        ax.imshow(img)
        # метод imshow принимает одно из двух:
        # - изображение в формате uint8, яркость от 0 до 255
        # - изображение в формате float, яркость от 0 до 1
        if labels:
            ax.set_title(f'Class: {label}')
    plt.show()


class DataGenerator:

    def __init__(self, path, img_size, bath_size, apply_aug=False, val_split=0.15, random_seed=15):
        self.apply_aug = apply_aug      # применить аугментацию (True, False)
        self.val_split = val_split      # доля данных для валидации (float)
        self.path = path                # путь к репозиторию с данными (str)
        self.img_size = img_size        # размер изображений в px (height, width)
        self.bath_size = bath_size      # размер батча (int)
        self.random_seed = random_seed  # random_seed (int)


    # аугментация и генерация данных для обучения
    def train_data_generator(self, subset):
        # subset - тип выборки для обучения ('training', 'validation')

        if self.apply_aug == False:
            datagen = ImageDataGenerator(
                validation_split=self.val_split,
            )

        else:
            # subset = (training, validation)
            datagen = ImageDataGenerator(
                # диапазон градусов для случайных поворотов
                rotation_range=15,
                # диапазон для сдвига яркости (список из 2-х значений), 0 - отсутствие яркости, 1 - стандартная яркость
                brightness_range=(0.5, 1.5),
                # cлучайный ввод сальто по горизонтали (отзеркаливание)
                horizontal_flip=True,
                # часть изображений, зарезервированных для проверки
                validation_split=self.val_split,
                # диапазон сдвига в ширину (%), остальная часть заполняется ближайшими соседями
                width_shift_range=0.15,
                # диапазон сдвига в высоту (%), остальная часть заполняется ближайшими соседями
                height_shift_range=0.15,
                # сдвиг под углом в указанном диапазоне - сильно меняет изображение в сравнении с rotation_range
                shear_range=15,
                # диапазон для случайного увеличения (как отдаляет, так и приближает изображение)
                zoom_range=0.15,
            )

        generator = datagen.flow_from_directory(
            # путь к папке с директориями групп изображений
            self.path,
            # изменить размер всех изображений
            target_size=self.img_size,
            # количество загружаемых картонок за 1 раз
            batch_size=self.bath_size,
            # выбрать классификацию
            class_mode='categorical',
            # перемешать данные
            shuffle=True,
            seed=self.random_seed,
            # обучающая выборка
            subset=subset
        )

        return(generator)


    # генерация данных для предикта
    def sub_data_generator(self, sample_submission_path):
        # sample_submission_path - путь к файлу для сабмита (str)
        
        # без изменений
        if self.apply_aug == False:
            datagen = ImageDataGenerator(
                #rescale=1/255
            )

        else:
            # применить аугментацию
            datagen = ImageDataGenerator(
                # диапазон градусов для случайных поворотов
                rotation_range=15,
                # диапазон для сдвига яркости (список из 2-х значений), 0 - отсутствие яркости, 1 - стандартная яркость
                brightness_range=(0.5, 1.5),
                # cлучайный ввод сальто по горизонтали (отзеркаливание)
                horizontal_flip=True,
                # часть изображений, зарезервированных для проверки
                # validation_split=VAL_SPLIT,
                # диапазон сдвига в ширину (%), остальная часть заполняется ближайшими соседями
                width_shift_range=0.15,
                # диапазон сдвига в высоту (%), остальная часть заполняется ближайшими соседями
                height_shift_range=0.15,
                # сдвиг под углом в указанном диапазоне - сильно меняет изображение в сравнении с rotation_range
                shear_range=15,
                # диапазон для случайного увеличения (как отдаляет, так и приближает изображение)
                zoom_range=0.15,
            )

        # формируем df и указываем пути к соответствующим изображениям для предсказания
        generator = datagen.flow_from_dataframe( 
            dataframe=pd.read_csv(sample_submission_path),
            # путь к каталогу с изображениям для предсказания
            directory=self.path,
            # содержит пути к файлам
            x_col="Id",
            # целевой признак
            y_col=None,
            class_mode=None,
            # изменить размер всех изображений
            target_size=self.img_size,
            # количество загружаемых картонок за 1 раз
            batch_size=self.bath_size,
            # не перемешивать данные
            shuffle=False
        )

        return(generator)