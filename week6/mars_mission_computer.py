import random
import time
import platform
import os
import psutil


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}, "
        log_entry += ', '.join(f"{key}: {value}" for key, value in self.env_values.items())

        with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + '\n')

        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.ds = DummySensor()
        self.data_log = []
        self.create_default_setting_file()

    def get_sensor_data(self):
        print('Press Ctrl+C to stop...')
        try:
            while True:
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                self.data_log.append(self.env_values.copy())

                print(self.env_values)
                if len(self.data_log) % 60 == 0:
                    self.calculate_five_min_avg()

                time.sleep(5)
        except KeyboardInterrupt:
            print('\nSystem stopped...')

    def calculate_five_min_avg(self):
        avg_values = {key: 0 for key in self.env_values.keys()}
        count = len(self.data_log[-60:])

        for entry in self.data_log[-60:]:
            for key in avg_values.keys():
                avg_values[key] += entry[key]

        for key in avg_values.keys():
            avg_values[key] /= count

        print('\nFive-Minute Average Values:')
        print(avg_values)

    def get_mission_computer_info(self):
        settings = self.read_settings().get('info', [])
        info = {}
        try:
            if 'operating_system' in settings:
                info['operating_system'] = platform.system()
            if 'os_version' in settings:
                info['os_version'] = platform.version()
            if 'cpu_type' in settings:
                info['cpu_type'] = platform.processor()
            if 'cpu_cores' in settings:
                info['cpu_cores'] = os.cpu_count()
            if 'memory' in settings:
                info['memory'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        except Exception as e:
            info['error'] = str(e)

        # get_mission_computer_info()에 가져온 시스템 정보를 JSON 형식으로 출력
        print('\nMission Computer Info:')
        print(info)

    # get_mission_computer_load() 메소드 만들고 MissionComputer 클래스에 추가
    def get_mission_computer_load(self):
        settings = self.read_settings().get('load', [])
        load = {}
        try:
            if 'cpu_usage' in settings:
                # CPU 실시간 사용량 가져오기
                load['cpu_usage'] = psutil.cpu_percent(interval=1)
            if 'memory_usage' in settings:
                # 메모리 실시간 사용량 가져오기
                load['memory_usage'] = psutil.virtual_memory().percent
        except Exception as e:
            load['error'] = str(e)

        print('\nMission Computer Load:')
        print(load)

    def read_settings(self):
        settings = {'info': [], 'load': []}
        try:
            with open('setting.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=')
                        settings[key] = [item.strip() for item in value.split(',')]
        except FileNotFoundError:
            print('setting.txt not found. Using default settings.')
        return settings

    def create_default_setting_file(self):
        if not os.path.exists('setting.txt'):
            with open('setting.txt', 'w', encoding='utf-8') as file:
                file.write('info=operating_system, os_version, cpu_type, cpu_cores, memory\n')
                file.write('load=cpu_usage, memory_usage\n')

# MissionComputer 클래스를 runComputer로 인스턴스화
runComputer = MissionComputer()

# get_mission_computer_info(), get_mission_computer_load() 호출해서 출력 확인
runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()
