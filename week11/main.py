# caesar_decoder.py

import string

# Caesar 암호 해독 함수
def caesar_cipher_decode(target_text):
    alphabet = string.ascii_lowercase
    dictionary = {"secret", "code", "the", "and", "password", "message", "attack", "decode", "hello", "world"}  # 간단한 텍스트 사전
    found = False

    print("[INFO] Caesar Cipher Decoding Attempts:")
    for shift in range(1, 26):  # 알파벳 수만큼 반복
        decoded = ""
        for char in target_text:
            if char in alphabet:
                index = (alphabet.index(char) - shift) % 26
                decoded += alphabet[index]
            else:
                decoded += char

        print(f"[{shift:2}] {decoded}")  # 자리수에 따라 해독된 결과 출력

        # 해독된 결과에서 사전 단어가 있는지 확인
        for word in dictionary:
            if word in decoded:
                print(f"[INFO] 사전 단어 \"{word}\" 발견 → 자동 중지 (자리수: {shift})")
                with open("result.txt", "w") as result_file:
                    result_file.write(decoded)
                found = True
                break

        if found:
            break

# 파일에서 password.txt 읽고 해독 시도
def main():
    try:
        with open("password.txt", "r") as f:
            encrypted = f.read().strip().lower()
            print(f"[INFO] password.txt 내용: {encrypted}")
            caesar_cipher_decode(encrypted)
    except FileNotFoundError:
        print("[ERROR] password.txt 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[ERROR] 예외 발생: {e}")

if __name__ == '__main__':
    main()
