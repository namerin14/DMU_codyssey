# main_bonus.py

import re  # 정규표현식 사용

# 사용자가 지정한 시간 리스트
target_times = ['10:35:00', '10:40:00']

try:
    with open('mission_computer_main.log', 'r') as log_file:
        log_data = log_file.readlines()

        # 전체 로그 역순 출력
        print('All Log List (Reversed Order) >>>>>')
        for line in reversed(log_data):
            print(line.strip(), '\n')

        # 지정된 시간에 해당하는 로그 필터링
        filtered_logs = []
        time_pattern = re.compile(r'\b\d{2}:\d{2}:\d{2}\b')
        
        for line in log_data:
            match = time_pattern.search(line)
            if match and match.group() in target_times:
                filtered_logs.append(line.strip())

        # 필터링된 로그 파일 저장
        with open('error_logs.log', 'w') as log_file:
            log_file.write('[ERROR LOGS]\n\n')
            if filtered_logs:
                for log in filtered_logs:
                    log_file.write(log + '\n')
            else:
                log_file.write('No error logs.\n')

        print('\nerror_logs.log file has been created.')

except FileNotFoundError:
    print('File not found.')
except Exception as e:
    print(f"except: {e}")
