# Car-classification
Классифицируем автомобиль по картинке

Соревнование kaggle (Rus_Salih_b) Top-25%: https://www.kaggle.com/competitions/sf-dl-car-classification

## Требования
Python 3.7.6

Зависимости: requirements.txt

## Данные и описание полей
**Соревновательные:**
https://www.kaggle.com/competitions/sf-dl-car-classification/data

**Дополнительные (собственная выгрузка):**
https://drive.google.com/file/d/1BGUHZpVscoJ_w_LtXFlz5QkedFwe_YNs/view?usp=sharing


## Обзор
### Изучим данные
**Распределение по классам:**
<img width="1361" alt="class" src="https://user-images.githubusercontent.com/73405095/196860136-e2ade3d0-024f-4502-937c-3a427efa05e9.png">

**Пример изображений:**
<img width="953" alt="image_sample" src="https://user-images.githubusercontent.com/73405095/197392956-bb8f6335-8098-49f9-9e24-197c1d44c6c8.png">

**Средний размер изображений:**
- mean_width:607.4 px
- mean_height:445 px

<br/>

### Применим легкую аугментацию к тренировочным данным
*Далее при изменении размера входных изображений будет применяться аугментации с такими же параметрами
<img width="1363" alt="aug_train" src="https://user-images.githubusercontent.com/73405095/197393055-9448929a-8b40-4287-a4bf-17788ff8bf9f.png">

<br/>

### Определим лучшую предобученную модель из SOTA
Размер изображений: (180, 240)

Критерий отбора тестирования: Необходима легковесная модель, но с высоким качеством на imagenet

Рассмотрим наиболее интересные модели из https://paperswithcode.com/sota/image-classification-on-imagenet

Обучим подходящие по критерию модели на 3-х эпохах с замороженными слоями, выберу лучшую по max val_accuracy

**Результат тестирования:**
<table>
  <tr>
    <th>Модель</th>
    <th>Описание</th>
    <th>best val_accuracy</th>
    <th>Комментарий</th>
  </tr>
  <tr>
    <td>ResNet50</td>
    <td>Легкая</td>
    <td>0.1301</td>
    <td>Не использовать</td>
  </tr>
    <tr>
    <td>EfficientNetB7</td>
    <td>Лучший результат на ImageNet из доступных</td>
    <td>0.9017</td>
    <td>Лучший результат</td>
  </tr>
  <tr>
    <td>MobileNetV3Large</td>
    <td>Самая легковесная, при этом высокое качество на ImageNet</td>
    <td>0.6891</td>
    <td>Не использовать</td>
  </tr>
  <tr>
    <td>EfficientNetV2L</td>
    <td>Высокий результат на ImageNet</td>
    <td>0.8703</td>
    <td>Возможно, протестировать</td>
  </tr>
  <tr>
    <td>ResNet152V2</td>
    <td>Легкая, с хорошим результатом</td>
    <td>0.1267</td>
    <td>Не использовать</td>
  </tr>
</table>

**Лучшая модель для задачи из протестированных является EfficientNetB7 - т.к. имеет наибольший val_accuracy**

<br/>

### Дополним датасет новыми данными
1. Загрузим новые изображения и объединим с основными:
<img width="360" alt="class_add_data" src="https://user-images.githubusercontent.com/73405095/197394335-cde81b60-e808-423d-868e-53c75632f07c.png">

2. Переобучим лучшую модель с новыми данными

val_accuracy: 0.8965

**Результат ухудшился, значит, для всего 10 классов датасет имеет достаточно изображений**

**Не используем далее новые данные**

<br/>

### Обучим нейросеть - step 1
Размер изображений: (220, 305)

1. Разморозим все слои сети

---

    base_model.trainable = True

2. Построим модель, добавив pooling и softmax слои на выходе
<img width="567" alt="model_layers" src="https://user-images.githubusercontent.com/73405095/197459643-109f5fc6-3473-4d15-9edd-3b07228c6782.png">

3. Настроим обучение модели, добавив в learning rate ExponentialDecay, для плавного снижения шага

---

    lr = ExponentialDecay(initial_learning_rate=1e-3, decay_steps=1000, decay_rate=0.9)


4. Настроим EarlyStopping, если модель не улучшается более 4 эпох и сохраним лучшую модель

---

    earlystop = EarlyStopping(monitor='val_accuracy', patience=4, restore_best_weights=True)

5. Обучим модель

Лучший результат val_accuracy: 0.9631

<br/>

### Обучим нейросеть - step 2
1. Увеличим размер изображений до (440px , 610px) - средний размер изображений
2. Загрузим лучшие веса из step 1

---

    model.load_weights('/content/drive/MyDrive/Analyst/data/Data science skill/Юнит 8. Нейронные сети/Проект 7. Ford vs Ferrari: определяем модель авто по фото/models/best_model2_val_accuracy_0.9622.hdf5')
  
3. Увеличим EarlyStopping до более 5-ти эпох и снизим learning rate
 
---

    lr = ExponentialDecay(initial_learning_rate=1e-6, decay_steps=1000, decay_rate=0.9)
    earlystop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)
  
4. Обучим модель

Лучший результат val_accuracy: 0.9734 (+1,03%)

<br/>

### Сделаем предсказание для соревнования на лучшей модели
- Результат: 0.97093

Применим аугментацию к тестовым изображениям (TTA)
- Результат: 0.97168



