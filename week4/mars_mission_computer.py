import random


# 1. 더미 센서에 해당하는 클래스를 생성한다. 클래스의 이름은 DummySensor로 정의한다. 
class DummySensor:
    # 2. DummySensor의 멤버로 env_values라는 사전 객체를 추가한다. 
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 화성 기지 내부 온도
            'mars_base_external_temperature': 0,  # 화성 기지 외부 온도
            'mars_base_internal_humidity': 0,  # 화성 기지 내부 습도
            'mars_base_external_illuminance': 0,  # 화성 기지 외부 광량
            'mars_base_internal_co2': 0,  # 화성 기지 내부 이산화탄소 농도
            'mars_base_internal_oxygen': 0  # 화성 기지 내부 산소 농도
        }

    # 3. DummySensor는 테스트를 위한 객체이므로 데이터를 램덤으로 생성한다. 
    # 4. DummySensor 클래스에 set_env() 메소드를 추가한다. 
    #    set_env() 메소드는 random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할을 한다.
    def set_env(self): 
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30) # randint: 정수 중 난수 리턴
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3) # uniform: 실수 중 난수 리턴 
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    # 5. DummySensor 클래스는 get_env() 메소드를 추가하는데 get_env() 메소드는 env_values를 return 한다. 
    def get_env(self):
        random_year = 2025 
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)  # 최소값으로 지정 (2월)
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        timestamp = f"{random_year}-{random_month:02d}-{random_day:02d} {random_hour:02d}:{random_minute:02d}:{random_second:02d}"

        # 로그 항목 생성 (타임스탬프 + 환경 변수 데이터)
        log_entry = f"[{timestamp}]\n"
        log_entry += '\n'.join(f"{key}: {value}" for key, value in self.env_values.items())

        # 로그 파일에 기록 (추가 모드 'a' 사용)
        with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + '\n')

        return self.env_values


ds = DummySensor() # 인스턴스 생성
ds.set_env() # 호출
current_env = ds.get_env()

# 환경 변수 출력
print('Current Environment Values:')
for key, value in current_env.items():
    print(f'{key}: {value}')
