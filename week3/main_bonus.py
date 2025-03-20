import struct

# 예외 처리: 파일 읽기
try:
    with open('Mars_Base_Inventory_List.csv', 'r') as file:
        lines = file.readlines()
except Exception as e:
    print(f"파일 읽기 오류: {e}")
    exit()

# 데이터 파싱
inventory_list = []
for line in lines[1:]:  # 첫 줄은 헤더
    items = line.strip().split(',')
    try:
        inventory_list.append({'substance': items[0], 'flammability': float(items[4])})
    except ValueError:
        continue

# 인화성 지수를 기준으로 내림차순 정렬
inventory_list.sort(key=lambda x: x['flammability'], reverse=True)

# 인화성 지수 0.7 이상 항목 출력
dangerous_items = [item for item in inventory_list if item['flammability'] >= 0.7]
for item in dangerous_items:
    print(item)

# CSV 파일 저장
try:
    with open('Mars_Base_Inventory_danger.csv', 'w') as file:
        file.write('substance,flammability\n')
        for item in dangerous_items:
            file.write(f"{item['substance']},{item['flammability']}\n")
except Exception as e:
    print(f"파일 저장 오류: {e}")
    exit()

# 보너스1: 이진 파일 저장
# text: 50바이트, float: 4바이트
try:
    with open('Mars_Base_Inventory_List.bin', 'wb') as bin_file:
        for item in inventory_list:
            bin_file.write(item['substance'].encode('utf-8').ljust(50, b'\x00'))  # 50바이트로 맞춤
            bin_file.write(struct.pack('f', item['flammability']))
except Exception as e:
    print(f"이진 파일 저장 오류: {e}")
    exit()

# 보너스2: 이진 파일 읽기
try:
    with open('Mars_Base_Inventory_List.bin', 'rb') as bin_file:
        while True:
            data = bin_file.read(50 + 4)
            if not data:
                break
            substance = data[:50].decode('utf-8').strip('\x00') # 50바이트 + null 삭제
            flammability = struct.unpack('f', data[50:])[0]
            print(f"substance: {substance}, flammability: {flammability}")
except Exception as e:
    print(f"이진 파일 읽기 오류: {e}")
    exit()

# 보너스3
# 텍스트 파일: 사람이 읽을 수 있는 문자 형식, 수정과 호환성이 용이하지만 저장 효율성이 낮고 속도가 느릴 수 있음.
# 이진 파일: 바이트 형식, 저장 효율성과 속도에 이점이 있지만, 사람이 읽을 수 없고 수정이 어려움.
