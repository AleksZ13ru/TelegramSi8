# inputs = [0, 3.0, 12.0, 13.0, 14.0, 14.0, 0, 0, 0, 1.0, 3.0, 5.0, 2.0, 4.0, 0]
"""
преобразование массива значения скорости в мин, в массив интервалов
"""


def min_to_time(sec):
    a = int(sec)
    h = (a // 60) % 60
    m = a % 60
    if h < 10:
        h = str('0' + str(h))
    if m < 10:
        m = str('0' + str(m))
    else:
        m = str(m)

    return str(h) + ':' + str(m)


def repack(name, date, inputs):
    position = 0
    start_pos = -1
    stop_pos = -1
    t_line = []
    r = []
    result = []
    for i in inputs:
        b = len(inputs)
        if i is not 0 and start_pos is -1:
            start_pos = position
        elif i is 0 and start_pos is not -1:
            stop_pos = position
        if position == len(inputs) - 1:
            stop_pos = position
        if start_pos is not -1 and stop_pos is not -1:
            for j in range(stop_pos - start_pos + 1):
                t_line.append(inputs[start_pos + j])
            r.append({'start': start_pos, 'v': t_line.copy()})
            start_pos = -1
            stop_pos = -1
            t_line.clear()
        position += 1
    total_l = 0
    string_l = []
    max_speed = 0
    max_speed_time = None
    summa_speed = 0
    summa_speed_count = 0
    for i in r:
        start_time = min_to_time(i['start'])
        stop_time = min_to_time(i['start'] + len(i['v']) - 1)
        vs = 0
        for index, v in enumerate(i['v']):
            vs = vs + v
            summa_speed = +vs
            summa_speed_count = +len(i['v'])
            if v >= max_speed:
                max_speed = v
                max_speed_time = min_to_time(i['start'] + index)
        string_l.append('{0} - {1} = {2:.0f} м.'.format(start_time, stop_time, vs))
        total_l = total_l + vs
    result.append("Оборудование: /{0}\n".format(name))
    result.append('Дата: {0}\n'.format(date.strftime("%d %B %Y")))
    result.append('Остановов: {0} \n'.format(len(r) - 1))
    result.append('Скорость:\n')
    result.append('  средняя: {0:.0f} м/мин. \n'.format(summa_speed/summa_speed_count))
    result.append('  макс.: {0:.2f} м/мин. в {1} \n'.format(max_speed, max_speed_time))
    result.append('Всего: {0:.0f} м.\n\n'.format(total_l))
    # result.append()
    for i in string_l:
        result.append(i + '\n')
    return result
