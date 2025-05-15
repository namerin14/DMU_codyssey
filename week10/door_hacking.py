import zipfile
import string
import time
from itertools import product
import os

def unlock_zip(zip_path='emergency_storage_key.zip'):
    charset = string.digits + string.ascii_lowercase  # 숫자 + 소문자
    max_length = 6
    attempt_count = 0
    start_time = time.time()

    try:
        with zipfile.ZipFile(zip_path) as zf:
            print("[INFO] Brute-force 시작...")
            
            for pwd_tuple in product(charset, repeat=max_length):
                password = ''.join(pwd_tuple)
                attempt_count += 1

                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    end_time = time.time()
                    print(f"[SUCCESS] 암호 발견: {password}")
                    print(f"[INFO] 시도 횟수: {attempt_count}")
                    print(f"[INFO] 소요 시간: {end_time - start_time:.2f}초")

                    # 성공 시 password.txt에 저장
                    with open("password.txt", "w") as f:
                        f.write(password)
                    return
                except:
                    # 실패한 경우는 무시
                    if attempt_count % 10000 == 0:
                        current_time = time.time()
                        print(f"[INFO] 시도: {attempt_count}회, 경과 시간: {current_time - start_time:.2f}초")

            print("[FAIL] 암호를 찾지 못했습니다.")

    except FileNotFoundError:
        print("[ERROR] zip 파일이 존재하지 않습니다.")
    except zipfile.BadZipFile:
        print("[ERROR] 올바르지 않은 zip 파일입니다.")
    except Exception as e:
        print(f"[ERROR] 예외 발생: {e}")


if __name__ == '__main__':
    unlock_zip()
