import re

from source.plot_utilities import circle_legend
from source.unity_performance_tests_data_transformer \
    import parse_xml, extract_radar_chart_data, adjust_ranges, add_units_for_metric_name, calculate_round_to_int

from mplsoccer import Radar, grid
import matplotlib.pyplot as plt


def plot_radar_chart(file_paths, file_names, output_root):
    data = parse_xml(file_paths)

    raw_metric_names, data_average, data_ranges, increase_is_better = extract_radar_chart_data(data)
    data_ranges = adjust_ranges(raw_metric_names, data_ranges, increase_is_better, inner_offset=0.2, outer_offset=0)
    metric_names = add_units_for_metric_name(data[0]['SampleGroups'])
    round_to_int = calculate_round_to_int(metric_names, data_ranges, range_labels_count=6)

    for metric_name, data_range in zip(metric_names, data_ranges):
        print(f"{metric_name.replace('\n', '').ljust(50)} range: {str(data_range).ljust(42)}" +
              f" int: {str(round_to_int[metric_name]).ljust(7)}" +
              f" average: {[average[metric_names.index(metric_name)] for average in data_average]}")

    radar = Radar(params=metric_names,
                  min_range=[range_min for range_min, range_max in data_ranges],
                  max_range=[range_max for range_min, range_max in data_ranges],
                  lower_is_better=[metric_name for metric_name, increase_is_better in
                                   zip(metric_names, increase_is_better) if not increase_is_better],
                  round_int=list(round_to_int.values()),
                  num_rings=6, ring_width=0.5, center_circle_radius=1.25)

    figure_size = 20.48

    fig, ax = grid(figheight=figure_size, grid_height=1, grid_width=0.98)
    radar.setup_axis(ax=ax)
    radar.draw_circles(ax=ax, facecolor='#F5F5F5', edgecolor='#F5F5F5')

    face_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, data in enumerate(data_average):
        radar.draw_radar_solid(data, ax=ax, kwargs={'facecolor': face_colors[i], 'alpha': 0.3})

    radar.draw_range_labels(ax=ax, fontsize=figure_size * 1.2)
    radar.draw_param_labels(ax=ax, fontsize=figure_size * 1.2, offset=0.5)

    circle_legend(ax,
                  labels=[re.sub(r'(.{10}) ', r'\1\n', ' '.join(re.findall(r'[A-Z][a-z]*', name)))
                          for name in file_names],
                  label_colors=face_colors,
                  circle_kwargs={'radius': 1.25, 'color': '#F5F5F5'},
                  text_kwargs={'fontsize': figure_size * 1.45,
                               'ha': 'center', 'va': 'center', 'alpha': 0.45, 'weight': 'bold'})

    output_file_name = 'Vs'.join(file_names) + f'RadarChart'
    plt.savefig(f'{output_root}//{output_file_name}.png')


def main():
    data_root = '../data/input/unity_tests/scene_space_rendering_vs_bounding_volumes_space_rendering/test_scene_1'
    output_root = '../data/output/unity_tests/scene_space_rendering_vs_bounding_volumes_space_rendering/test_scene_1'
    file_names = ['SceneSpaceRendering', 'BoundingVolumesSpaceRendering']
    file_paths = [f"{data_root}//{file_name}" for file_name in file_names]

    plot_radar_chart(file_paths, file_names, output_root)


if __name__ == '__main__':
    main()
