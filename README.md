Предсказание поломки оборудования
Цель: Нужно предсказать, произойдёт ли отказ оборудования на основе его технических характеристик, условий эксплуатации и истории работы.

Расшифровка столбцов датасета

Идентификаторы:

id - Уникальный числовой идентификатор записи
Product ID - Идентификатор продукта/оборудования (формат: буква + цифры)
Type - Тип оборудования (категория: L, M, H - Low/Medium/High)
Технологические параметры:
Air temperature [K] - Температура окружающего воздуха в Кельвинах
Process temperature [K] - Технологическая температура процесса в Кельвинах
Rotational speed [rpm] - Скорость вращения в оборотах в минуту
Torque [Nm] - Крутящий момент в Ньютон-метрах
Tool wear [min] - Износ инструмента в минутах работы
Признаки отказов:

Machine failure - Общий индикатор отказа оборудования (1 - отказ, 0 - норма)
TWF - Tool Wear Failure (Отказ из-за износа инструмента)
HDF - Heat Dissipation Failure (Отказ теплоотвода)
PWF - Power Failure (Отказ питания)
OSF - Overstrain Failure (Отказ из-за перегрузки)
RNF - Random Failures (Случайные отказы)

Выводы:

1 Проведен исследовательский анализ данных.

2 Созданы новые признаки:\

'HDF_temp' - разница признаков 'Process temperature [K]' и 'Air temperature [K]'\
'PWF_n' - произведение признаков 'Torque [Nm]' и 'Rotational speed [rpm]'\
'OSF_n' - произведение признаков 'Torque [Nm]' и 'Tool wear [min]'
3 Обнаружены следующие зависимости в данных нормального состояния (0) и отказа (1):\ 3.1 TWF - Tool Wear Failure (Отказ из-за износа инструмента):\

Tool wear [min] - 0: Q25-Q75: 53-162, 1: Q25-Q75: 198-26
3.2 HDF - Heat Dissipation Failure (Отказ теплоотвода):\

Air temperature [K] - 0: Q25-Q75: 298.3-301.5, 1: Q25-Q75: 302.1-303.075\
Rotational speed [rpm] - 0: Q25-Q75: 1426-1614, 1: Q25-Q75: 1259-1379\
Torque [Nm] - 0: Q25-Q75: 33.1-46.6, 1: Q25-Q75: 48.2-57.1\
HDF_temp: Q25-Q75: 9.3-11, 1: Q25-Q75: 7.6-8.6
3.4 PWF - Power Failure (Отказ питания):\

Rotational speed [rpm] - 0: Q25-Q75: 1424-1611, 1: Q25-Q75: 1312-2563.75\
Tool wear [min] - 0: Q25-Q75: 52-161, 1: Q25-Q75: 172-238\
PWF_n - 0: Q25-Q75: 885.6-1112.2, 1: Q25-Q75: 546.8-1494
3.5 OSF - Overstrain Failure (Отказ из-за перегрузки):\

Tool wear [min] - 0: Q25-Q75: 52-161, 1: Q25-Q75: 172-238\
Torque [Nm] - 0: Q25-Q75: 33.1-46.6, 1: Q25-Q75: 46.3-70.5\
OSF_n - 0: Q25-Q75: 1846.87-6232.8, 1: Q25-Q75: 110032.8-16479
4 Сгенерированы новые признаки:
4.1 TW_cat (признак Tool wear [min] больше или меньше 198)
4.2 AT_cat (признак Air temperature [K] больше или меньше 301.6)
4.3 HDF_cat - комбинация признаков HDF_temp (больше или меньше 8.7) и 'Rotational speed [rpm]' (больше или меньше < 1380)
4.4 PWF_cat - (признак PWF_n > 885.5 и < 1112.3)

5 Проведен корреляционный анализ данных - признаки с мультиколлинеарностью удалены.

6 Обучено несколько моделей с перебором гипрепраметров. Целевая метрика - f1 (т.к. мы хотим посмотреть на баланс метрик recall и precision), целевой признак - Machine failure. Лучшей моделью является LGBMClassifier: Parameters boosting_type 'gbdt' num_leaves 118 max_depth 2 learning_rate 0.2 n_estimators 125 subsample_for_bin 200000 objective None class_weight None min_split_gain 0.0 min_child_weight 0.001 min_child_samples 1 subsample 1.0 subsample_freq 0 colsample_bytree 1.0 reg_alpha 0.0 reg_lambda 0.0 random_state 42 n_jobs None importance_type 'split' verbose -1

'Метрики по результатам тестовой выборки:'
'F1 score: 0.7974'
'F2 score: 0.7475'
'Accuracy: 0.9876'
'Recall: 0.7176'
'Precision: 0.8971'
'ROC AUC: 0.8574'
'MCC: 0.796'

7 Оценена важность признаков:
7.1 Rotation speed (0.91) - чем она меньше, тем выше риск поломки.
7.2 PWF_cat (0.72) - если равно 1, вероятность поломки выше.
7.3 Tool Wear (0.52) - чем фактор выше, тем выше риск поломки.
7.4 HDF_temp (0.31) - чем фактор ниже, тем выше риск поломки.
7.5 Process Tempurature (0.21) - чем фактор ниже, тем выше риск поломки.
