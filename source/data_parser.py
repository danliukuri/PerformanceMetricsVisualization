from bs4 import BeautifulSoup
import json


def parse_unity_performance_tests_xml(file_paths):
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