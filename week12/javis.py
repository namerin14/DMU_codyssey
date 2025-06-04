import os
import datetime
import wave
import pyaudio

def ensure_records_directory():
    """Ensure the 'records' directory exists."""
    if not os.path.exists('records'):
        os.makedirs('records')

def generate_filename():
    """Generate filename based on current date and time."""
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S') + '.wav'

def record_audio(duration=5):
    """Record audio from microphone for a given duration in seconds."""
    ensure_records_directory()
    filename = os.path.join('records', generate_filename())

    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100

    pa = pyaudio.PyAudio()

    try:
        print('[INFO] 녹음을 시작합니다...')
        stream = pa.open(format=sample_format,
                         channels=channels,
                         rate=rate,
                         frames_per_buffer=chunk,
                         input=True)

        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        pa.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pa.get_sample_size(sample_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print(f'[INFO] 녹음이 완료되었습니다: {filename}')

    except Exception as e:
        print(f'[ERROR] 녹음 중 오류 발생: {e}')

def list_recordings(start_date, end_date):
    """List recordings between start_date and end_date (inclusive)."""
    try:
        if not os.path.exists('records'):
            print('[INFO] 기록된 파일이 없습니다.')
            return

        start = datetime.datetime.strptime(start_date, '%Y%m%d')
        end = datetime.datetime.strptime(end_date, '%Y%m%d')

        files = os.listdir('records')
        filtered = []

        for file in files:
            try:
                timestamp_str = file.split('.')[0]
                file_date = datetime.datetime.strptime(timestamp_str, '%Y%m%d-%H%M%S')
                if start <= file_date <= end:
                    filtered.append(file)
            except Exception:
                continue

        print(f'[INFO] {start_date} ~ {end_date} 사이의 녹음 파일:')
        for f in sorted(filtered):
            print('  -', f)

    except Exception as e:
        print(f'[ERROR] 날짜 범위 필터링 중 오류 발생: {e}')

if __name__ == '__main__':
    # 예시 실행
    record_audio(duration=5)  # 5초간 녹음
    list_recordings('20250101', '20251231')  # 2025년 전체 녹음 목록 출력
