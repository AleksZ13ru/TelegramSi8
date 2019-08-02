# import svgwrite
from si8_parsing.code.pack import min_to_time
from si8_parsing.models import Party
from django.utils import timezone
import datetime
from django.core.exceptions import ObjectDoesNotExist
# dwg = svgwrite.Drawing('svgwrite-example.svg', profile='tiny', size=(200, 20))

# draw a red box
# data-toggle="tooltip" title="08:00 - 12"
# dwg.add(dwg.rect((0, 0), (2, 20), fill='red', data_toggle='tooltip', title="08:00-12"))
# dwg.save()

color_100 = '#C8E6C9'
color_200 = '#A5D6A7'
color_300 = '#81C784'
color_400 = '#66BB6A'
color_500 = '#4CAF50'
color_600 = '#43A047'
color_700 = '#388E3C'
color_800 = '#2E7D32'
color_900 = '#1B5E20'

svg_text_start = '<svg version="1.1" class="img-fluid" baseProfile="full" width="1440" height="20" xmlns="http://www.w3.org/2000/svg">'
svg_text_stop = '</svg>'
svg_text_rect_default = '<rect data-toggle="tooltip" title="08:00 - 12" height="20" width="20" fill="#81C784" ></rect>'

input_dates = [5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.3, 5.5,
               5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6,
               5.5, 5.6, 5.5, 5.5, 6.0, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0,
               6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1,
               6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1,
               6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1, 6.0, 6.1, 6.0, 6.1, 6.0, 6.1, 6.0, 6.1, 6.0, 6.0, 6.1,
               6.0, 6.1, 6.0, 6.0, 5.6, 5.5, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5,
               5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5,
               5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5,
               5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5,
               5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5,
               5.6, 5.5, 5.5, 5.6, 5.5, 5.6, 5.5, 5.6, 5.9, 15.1, 5.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 31.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0.9, 1.1, 0, 0, 0,
               0.4, 0.9, 3.3, 4.0, 4.0, 4.1, 3.4, 4.1, 4.0, 4.1, 4.0, 4.0, 4.0, 4.1, 4.8, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0,
               5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0,
               5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.0, 5.1, 5.0, 5.0, 5.1, 5.0, 5.0, 5.0, 5.1, 5.0, 5.0, 5.3, 6.3,
               7.2, 7.6, 7.8, 8.1, 8.0, 8.0, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6,
               8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5,
               8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5,
               8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6,
               8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5, 8.6, 8.5, 8.6, 8.5, 8.6, 8.5, 8.5,
               8.6, 8.5, 8.6, 8.5, 8.6, 8.6, 8.6, 1.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.7, 5.3, 24.2, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.9, 2.4, 0, 0, 1.7, 4.0, 4.0, 4.1, 4.0, 4.0, 4.1,
               4.0, 4.0, 4.0, 4.1, 4.0, 4.0, 5.3, 6.0, 6.0, 6.1, 7.0, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0,
               7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1,
               7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0,
               7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0,
               7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0,
               7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.1,
               7.1, 7.0, 1.5, 0, 0, 0, 0, 22.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.3, 0.8,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.8, 4.1, 4.0, 4.0, 4.1, 4.0, 4.0, 4.1, 4.0, 4.0, 4.0, 4.1, 4.2, 5.3,
               6.0, 6.9, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0,
               7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1,
               7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0,
               7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0,
               7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0,
               7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0,
               7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1,
               7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.1, 7.0, 7.0, 7.1, 7.0, 7.0, 7.0, 7.1, 7.0, 7.0, 7.1,
               7.1, 7.0, 7.1, 2.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16.9, 13.2]


# svg_text_full = svg_text_start + svg_text_rect + svg_text_stop
def addMinute(tm, minutes):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(minutes=minutes)
    return fulldate.time()


def rect_create(x, title, color):
    result = '<rect data-toggle="tooltip" title="{0}" \
    height="20" width="1" x="{1}" y="0" fill="{2}"/>'.format(title, x, color)
    return result


TIME_FORMAT = '%H:%M'


def svg_text_create(values=None, party=0, next_values=None):
    svg_text_rects = ''
    try:
        p = Party.objects.get(index=party)
        j = 0
        for i in values:
            color = color_100
            if i > 0.0:
                color = color_500
            title = '{0} - {1}'.format(addMinute(p.time_start, j).strftime(TIME_FORMAT), i)
            svg_text_rects = svg_text_rects + rect_create(x=j, title=title, color=color)
            j = j + 1

        svg_text_full = svg_text_start + svg_text_rects + svg_text_stop
        return svg_text_full
    except ObjectDoesNotExist:
        return svg_pure()


# TODO: удалить!
def svg_text_create0(values=None, party=0, next_values=None):
    svg_text_rects = ''
    j = 0
    for i in values:
        color = color_100
        if i > 0.0:
            color = color_500
        # if i > 25.0:
        #     color = color_500
        # if i > 10.0:
        #     color = color_700
        # if i > 20.0:
        #     color = color_900
        title = '{0} - {1}'.format(min_to_time(j), i)
        if (party is 0):
            svg_text_rects = svg_text_rects + rect_create(x=j, title=title, color=color)
        elif (party is 1) and (j >= 440) and (j <= 1120):
            svg_text_rects = svg_text_rects + rect_create(x=j - 440, title=title, color=color)
        elif (party is 2) and (j >= 1120):
            svg_text_rects = svg_text_rects + rect_create(x=j-1120, title=title, color=color)
        j = j + 1
    if party is 2:
        title = '{0} - {1}'.format(min_to_time(j), i)
        j=0
        for i in next_values:
            color = color_100
            if i > 0.0:
                color = color_500
            title = '{0} - {1}'.format(min_to_time(j), i)
            if j < 440:
                svg_text_rects = svg_text_rects + rect_create(x=j+320, title=title, color=color)
            j = j + 1
    svg_text_full = svg_text_start + svg_text_rects + svg_text_stop
    return svg_text_full


# def svg_text_create(values=input_dates):
#     svg_text_rects = ''
#     j = 0
#     for i in values:
#         color = color_100
#         if i > 0.0:
#             color = color_500
#         # if i > 25.0:
#         #     color = color_500
#         # if i > 10.0:
#         #     color = color_700
#         # if i > 20.0:
#         #     color = color_900
#
#         title = '{0} - {1}'.format(min_to_time(j), i)
#         svg_text_rects = svg_text_rects + rect_create(x=j, title=title, color=color)
#         j = j + 1
#
#     svg_text_full = svg_text_start + svg_text_rects + svg_text_stop
#     return svg_text_full


def svg_pure():
    svg_text_full = svg_text_start + svg_text_stop
    return svg_text_full


def svg_file_create():
    f = open('text.svg', 'w')
    f.write(svg_text_create())
    f.close()

