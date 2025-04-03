import random
import time

class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {}
        self.data_log = []

    def get_sensor_data(self):
        try:
            while True:
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                self.data_log.append(self.env_values)

                print(self.env_values)
                
                if len(self.data_log) % 60 == 0: # 5초 x 60 = 300초 (5분)
                    self.calculate_five_min_avg()
                
                time.sleep(5)
        except KeyboardInterrupt: # ctrl + c
            print('System stopped...')

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
        log_entry = f"\n{timestamp}\n"
        log_entry += '\n'.join(f"{key}: {value}" for key, value in self.env_values.items())

        with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + '\n')

        return self.env_values



RunComputer = MissionComputer()
RunComputer.get_sensor_data()
