import shutil
import os
import zipfile


# объединить новые данные с основными в новом репозитории, вернуть путь к репозиторию
def add_data(path_rep, concat_rep_name, path_new_data, name_new_data, path_base_data):
  # path_rep - путь к корню проекта (path_rep)
  # concat_rep_name - название папки, в которой будут объеденены старые и новые данные (big_data)
  # path_new_data - название папки с архивом новых данных (папка должна находиться внутри проект) (add_train)
  # name_new_data - название архива (add_train) - вводить без расширения, принимает только .zip
  # path_base_data - путь к разархивированным тренировочным данным (data/temp/train)

  # создадим директорию для общего датасета
  os.mkdir(f'{path_rep}/{concat_rep_name}')
  for i in range(10):
    os.mkdir(f'{path_rep}/{concat_rep_name}/{i}')

  # разархивировал датасет в директорию
  archive = f'{path_rep}/{path_new_data}/{name_new_data}.zip'
  with zipfile.ZipFile(archive, 'r') as zip_file:
    zip_file.extractall(f'{path_rep}/{path_new_data}/temp')

  # выгрузим из дополнительного датасета данные в общий датасет
  for i in range(10):
    source =f'{path_rep}/{path_new_data}/temp/{name_new_data}/{i}/'
    dest1 = f'{path_rep}/{concat_rep_name}/{i}/'
    files = os.listdir(source)
    for f in files:
      shutil.copy(source+f, dest1)


  # выгрузим из train датасета данные в общий датасет
  for i in range(10):
    source = f'{path_rep}/{path_base_data}/{i}/'
    dest1 = f'{path_rep}/{concat_rep_name}/{i}/'


    files = os.listdir(source)

    for f in files:
      shutil.copy(source+f, dest1)

  # удалить файлы не с форматом jpg
  for i in range(10):
    dir_name = f'{path_rep}/{concat_rep_name}/{i}/'
    test = os.listdir(dir_name)

    for item in test:
        if not item.endswith(".jpg"):
            try:
              os.remove(os.path.join(dir_name, item))
            except:
              pass

  # задаем новый путь к дополненному датасету
  train_big_path = f'{path_rep}/{concat_rep_name}/'

  return(train_big_path)

