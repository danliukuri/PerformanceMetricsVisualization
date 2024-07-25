import re

import numpy as np
from bs4 import BeautifulSoup
import json


def parse_xml(file_paths):
    result_data = []

    for file_path in file_paths:
        with open(file_path + '.xml', encoding="utf8") as file:
            xml_data = file.read()
        soup = BeautifulSoup(xml_data, 'xml')
        raw_data = soup.find('output').get_text()
        data_start_index = raw_data.index('{')
        data_end_index = raw_data.index('\n##performancetestruninfo2')
        data = raw_data[data_start_index:data_end_index]
        result_data.append(json.loads(data))

    return result_data


def extract_radar_chart_data(parsed_data):
    num_metrics = len(parsed_data[0]['SampleGroups'])

    metric_names = []
    data_average = [[] for _ in range(len(parsed_data))]
    data_ranges = []
    increase_is_better = []

    for i in range(num_metrics):
        metric_names.append(parsed_data[0]['SampleGroups'][i]['Name'])
        metric_averages = []

        for j, dataset in enumerate(parsed_data):
            samples = dataset['SampleGroups'][i]['Samples']
            avg = np.mean(samples)
            metric_averages.append(avg)
            data_average[j].append(avg)

        data_ranges.append(((min(metric_averages)), (max(metric_averages))))
        increase_is_better.append(parsed_data[0]['SampleGroups'][i]['IncreaseIsBetter'])

    return metric_names, data_average, data_ranges, increase_is_better


def add_units_for_metric_name(sample_groups, explicit_unit_format=r'\s?\(?{}\)?', unit_format=f' \n({{0}})'):
    metric_names_and_units = []
    explicit_units = ['Bytes', 'Count', 'FPS']
    units = ['Nanoseconds', 'Microseconds', 'Milliseconds', 'Seconds', 'Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes',
             'Undefined']

    for sample_group in sample_groups:
        metric_name_and_unit = name = sample_group['Name']

        if any(unit in name for unit in explicit_units):
            for unit in explicit_units:
                if unit in name:
                    metric_name_and_unit = re.sub(explicit_unit_format.format(unit), unit_format.format(unit), name)
        else:
            metric_name_and_unit += unit_format.format(units[sample_group['Unit']])

        metric_names_and_units.append(metric_name_and_unit)

    return metric_names_and_units


def adjust_ranges(raw_metric_names, data_ranges, increase_is_better, inner_offset=0, outer_offset=0):
    new_ranges = []

    ranges_min_length = {
        'Test Duration': 50,
        'Frame Time': 10,
        'Framerate (FPS)': 50,
        'CPU Total Frame Time': 15,
        'CPU Render Thread Frame Time': 0.25,
        'GPU Frame Time': 10,
        'SetPass Calls Count': 15,
        'Draw Calls Count': 15,
        'Batches Count': 15,
        'Triangles Count': 2500,
        'Vertices Count': 1500,
        'Vertex Buffer Upload In Frame Count': 10,
        'Vertex Buffer Upload In Frame Bytes': 800,
        'Index Buffer Upload In Frame Count': 10,
        'Index Buffer Upload In Frame Bytes': 60+90,
        'Actual framerate (FPS)': 50,
        'Used Buffers Count': 10,
        'Used Buffers Bytes': 5,
        'Material Memory': 5,
        'Gfx Used Memory': 0.6,
        'Mesh Memory': 15
    }

    ranges_shift = {
        'Test Duration': -15.0254029500000065,
        'Frame Time': 1-0.054587755484327,
        'Framerate (FPS)': 2-0.765525701734545,
        'CPU Total Frame Time': -0.5545939805139255,
        'CPU Render Thread Frame Time': 0.07,
        'GPU Frame Time': 2-0.51464842189748,
        'SetPass Calls Count': 3.5,
        'Draw Calls Count': 2.5,
        'Batches Count': 2.5,
        'Triangles Count': 163,
        'Vertices Count': 16,
        'Vertex Buffer Upload In Frame Count': 1.5,
        'Vertex Buffer Upload In Frame Bytes': -4,
        'Index Buffer Upload In Frame Count': 1.5,
        'Index Buffer Upload In Frame Bytes': 33,
        'Actual framerate (FPS)': 2-0.50088497797648,
        'Used Buffers Count': 1,
        'Used Buffers Bytes': 2-0.59199999999998,
        'Material Memory': 1-0.306,
        'Gfx Used Memory': 0.07,
        'Mesh Memory': 7-0.744
    }

    for i in range(len(data_ranges)):
        min_avg, max_avg = data_ranges[i]

        metric_inner_offset, metric_outer_offset = inner_offset, outer_offset
        if not increase_is_better[i]:
            metric_inner_offset, metric_outer_offset = outer_offset, inner_offset

        range_length = max_avg - min_avg

        if range_length < ranges_min_length[raw_metric_names[i]]:
            min_avg -= (ranges_min_length[raw_metric_names[i]] - range_length) / 2
            max_avg += (ranges_min_length[raw_metric_names[i]] - range_length) / 2

        range_length = max_avg - min_avg
        buffer_min = metric_inner_offset * range_length - ranges_shift[raw_metric_names[i]]
        buffer_max = metric_outer_offset * range_length + ranges_shift[raw_metric_names[i]]

        new_ranges.append((min_avg - buffer_min, max_avg + buffer_max))
    return new_ranges


def calculate_round_to_int(metric_names, data_ranges, range_labels_count):
    round_to_int = {}
    for name, (min_val, max_val) in zip(metric_names, data_ranges):
        step = (max_val - min_val) / range_labels_count
        round_to_int[name] = all(val.is_integer() for val in [min_val, max_val, step])
    return round_to_int
