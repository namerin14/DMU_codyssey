import os
import wave
import csv
import pyaudio
import datetime
import speech_recognition as sr


RECORDS_DIR = 'records'
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def ensure_records_dir():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)


def record_audio(duration=5):
    ensure_records_dir()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print('[INFO] 녹음 시작...')
    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    print('[INFO] 녹음 종료.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = os.path.join(RECORDS_DIR, f'{timestamp}.wav')

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f'[INFO] 파일 저장: {filename}')
    return filename


def list_audio_files(start_date=None, end_date=None):
    ensure_records_dir()
    files = os.listdir(RECORDS_DIR)
    wav_files = [f for f in files if f.endswith('.wav')]
    if start_date and end_date:
        filtered = []
        for f in wav_files:
            date_part = f.split('.')[0].split('-')[0]
            if start_date <= date_part <= end_date:
                filtered.append(f)
        return filtered
    return wav_files


def stt_process(filename):
    recognizer = sr.Recognizer()
    audio_path = os.path.join(RECORDS_DIR, filename)
    csv_path = os.path.join(RECORDS_DIR, filename.replace('.wav', '.csv'))

    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            print(f'[INFO] {filename} STT 처리 중...')
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f'[RESULT] {text}')

            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Text'])
                writer.writerow(['0.0', text])

            print(f'[INFO] CSV 저장 완료: {csv_path}')

    except sr.UnknownValueError:
        print(f'[WARN] 인식 실패: {filename}')
    except sr.RequestError as e:
        print(f'[ERROR] STT 요청 오류: {e}')
    except FileNotFoundError:
        print(f'[ERROR] 파일 없음: {audio_path}')


def search_keyword_in_csv(keyword):
    ensure_records_dir()
    files = [f for f in os.listdir(RECORDS_DIR) if f.endswith('.csv')]
    for file in files:
        path = os.path.join(RECORDS_DIR, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 스킵
                for row in reader:
                    if keyword in row[1]:
                        print(f'[FOUND] {file} -> {row}')
        except Exception as e:
            print(f'[ERROR] {file} 읽기 오류: {e}')


if __name__ == '__main__':
    ensure_records_dir()
    while True:
        print('\n1. 음성 녹음')
        print('2. 녹음 목록 조회')
        print('3. STT 실행')
        print('4. 키워드 검색')
        print('5. 종료')
        choice = input('선택: ')

        if choice == '1':
            record_audio()
        elif choice == '2':
            start = input('시작일 (YYYYMMDD, 생략 시 전체): ')
            end = input('종료일 (YYYYMMDD, 생략 시 전체): ')
            files = list_audio_files(start if start else None, end if end else None)
            print('[목록]')
            for f in files:
                print(f)
        elif choice == '3':
            name = input('STT 처리할 파일명 입력 (.wav 포함): ')
            stt_process(name)
        elif choice == '4':
            word = input('검색할 키워드 입력: ')
            search_keyword_in_csv(word)
        elif choice == '5':
            break
        else:
            print('[ERROR] 올바른 번호를 선택하세요.')
