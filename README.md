# Car-classification
Классифицируем автомобиль по картинке
Соревнование kaggle (Rus_Salih_b) Top-25%: https://www.kaggle.com/competitions/sf-dl-car-classification

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

### Применим легкую аугментацию к тренировочным данным
<img width="1363" alt="aug_train" src="https://user-images.githubusercontent.com/73405095/197393055-9448929a-8b40-4287-a4bf-17788ff8bf9f.png">

### Определим лучшую предобученныую модель из SOTA
Критерий отбора: Необходима легковесная модель, но с высоким качеством на imagenet

Рассмотрю наиболее интересные модели из https://paperswithcode.com/sota/image-classification-on-imagenet

Обучу подходящие по критерию модели на 3-х эпохах с замороженными слоями, выберу лучшую по max val_accuracy

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
    <td>лучший результат на ImageNet из доступных</td>
    <td>0.9017</td>
    <td>Лучший результат</td>
  </tr>
  <tr>
    <td>MobileNetV3Large</td>
    <td>самая легковесная, при этом высокое качетсво на ImageNet</td>
    <td>0.6891</td>
    <td>Не использовать</td>
  </tr>
  <tr>
    <td>EfficientNetV2L</td>
    <td>отличный результат на ImageNet</td>
    <td>0.8703</td>
    <td>Возможно, протестировать</td>
  </tr>
  <tr>
    <td>ResNet152V2</td>
    <td>легкая, с хорошим результатом</td>
    <td>0.1267</td>
    <td>Не использовать</td>
  </tr>
</table>

**Лучшая модель для задачи из протестированных является EfficientNetB7 - т.к. имеет наибольший val_accuracy**

### Дополним датафрейм новыми данными
1. Загрузим новые изображения и объединим с основными:
<img width="360" alt="class_add_data" src="https://user-images.githubusercontent.com/73405095/197394335-cde81b60-e808-423d-868e-53c75632f07c.png">

2. Проведем аугментацию

3. Переобучим лучшую модель с новыми данными

val_accuracy: 0.8965

**Результат ухудшился, значит, для всего 10 классов датасет имеет достаточно изображений. Не используем новые данные.**



