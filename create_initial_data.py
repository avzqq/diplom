import csv


def data_initialization():
    """ У каждого вида ремонта есть от одного до трёх вариантов периодичности.
    Например, у ТР-1 это либо 225, либо 180 суток.
    У некоторых тепловозов совпадают варианты ТР-1, ТР-2 и т.д. и я собираю
    их в группу.
    Например, у ТЭМ и ТЭМ2У текущий ремонт 1 проводится раз в 225 суток,
    поэтому они идут в группу "а". У ТГМ4(A) и ТГМ4 текущий ремонт 1
    проводится раз в 180 суток, поэтому они идут в группу "б" и т.д.
    Функция делает четыре  шага:
    1. Создаёт модели тепловозов в виде словарей, пока только с названием.
    2. Разбивает их на группы.
    3. Описывает виды ремонтов с возможными вариантами периодичности.
    4. Каждому тепловозу определенной группы записывает подходящий вариант
        периодичности для каждого ремонта.
    В конце упаковывает все тепловозы в один список для возвращения.
    """
    tam = {"loco_model_name": "ТЭМ"}
    tam2y = {"loco_model_name": "ТЭМ2У"}
    tam2m = {"loco_model_name": "ТЭМ2М"}
    tam2ym = {"loco_model_name": "ТЭМ2УМ"}
    tam15 = {"loco_model_name": "ТЭМ15"}
    tam18 = {"loco_model_name": "ТЭМ18"}

    tgm4_a = {"loco_model_name": "ТГМ4(А)"}
    tgm4 = {"loco_model_name": "ТГМ4"}
    tgm4a = {"loco_model_name": "ТГМ4А"}

    tgm4_b = {"loco_model_name": "ТГМ4(Б)"}
    tgm4b = {"loco_model_name": "ТГМ4Б"}
    tgm4bl = {"loco_model_name": "ТГМ4Бл"}

    group_a = [tam, tam2y, tam2m, tam2ym, tam15, tam18]
    group_b = [tgm4_a, tgm4, tgm4a]
    group_c = [tgm4_b, tgm4b, tgm4bl]

    three_maintenance = {"0": 30}
    one_current_repair = {"0": 225, "1": 180}
    two_current_repair = {"0": 450, "1": 540, "2": 900}
    three_current_repair = {"0": 900, "1": 1080, "2": 1800}
    medium_repair = {"0": 2160, "1": 2700}
    overhaul = {"0": 4320, "1": 5400}

    for loco in group_a:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["0"]
        loco["two_current_repair"] = two_current_repair["0"]
        loco["three_current_repair"] = three_current_repair["0"]
        loco["medium_repair"] = medium_repair["0"]
        loco["overhaul"] = overhaul["0"]

    for loco in group_b:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["1"]
        loco["two_current_repair"] = two_current_repair["1"]
        loco["three_current_repair"] = three_current_repair["1"]
        loco["medium_repair"] = medium_repair["0"]
        loco["overhaul"] = overhaul["0"]

    for loco in group_c:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["1"]
        loco["two_current_repair"] = two_current_repair["2"]
        loco["three_current_repair"] = three_current_repair["2"]
        loco["medium_repair"] = medium_repair["1"]
        loco["overhaul"] = overhaul["1"]

    all_data = [*group_a, *group_b, *group_c]
    keys = group_a[0].keys()
    return all_data, keys


def generate_csv():
    list_of_models, fields = data_initialization()
    with open('initial_data.csv', 'w', encoding='UTF-8') as f:
        writer = csv.DictWriter(f, fields, delimiter=';')
        writer.writeheader()
        for model in list_of_models:
            writer.writerow(model)


if __name__ == "__main__":
    generate_csv()
