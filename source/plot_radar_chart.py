import re

from source.plot_utilities import circle_legend
from source.unity_performance_tests_data_transformer \
    import parse_xml, extract_radar_chart_data, adjust_ranges, add_units_for_metric_name, calculate_round_to_int


def plot_radar_chart(file_paths):
    data = parse_xml(file_paths)

    raw_metric_names, data_average, data_ranges, increase_is_better = extract_radar_chart_data(data)
    data_ranges = adjust_ranges(raw_metric_names, data_ranges, increase_is_better, inner_offset=0.2, outer_offset=0)
    metric_names = add_units_for_metric_name(data[0]['SampleGroups'])
    round_to_int = calculate_round_to_int(metric_names, data_ranges, range_labels_count=6)

    for metric_name, data_range in zip(metric_names, data_ranges):
        print(f"{metric_name.replace('\n', '').ljust(50)} range: {str(data_range).ljust(42)}" +
              f" int: {str(round_to_int[metric_name]).ljust(7)}" +
              f" average: {[average[metric_names.index(metric_name)] for average in data_average]}")

def main():
    data_root = '../data/input/unity_tests'
    file_names = ['SceneRendering', 'VolumetricRendering']
    file_paths = [f"{data_root}//{file_name}" for file_name in file_names]

    plot_radar_chart(file_paths)


if __name__ == '__main__':
    main()
