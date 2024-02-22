from source.data_parser import parse_unity_performance_tests_xml

if __name__ == '__main__':
    data_root = '../data/sources/unity_tests'
    file_names = ['SceneRendering', 'VolumetricRendering']

    data = parse_unity_performance_tests_xml([f"{data_root}/{file_name}" for file_name in file_names])

    print(data)