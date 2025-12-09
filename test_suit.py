import sys
import os
import shutil
import numpy as np
from PIL import Image
import contextlib

# 내부 모듈의 print 문 출력을 억제하기...
@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# src 폴더 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_tests():
    errors = []

    # stdout 출력을 막고 테스트 실행
    with suppress_stdout():
        try:
            # 모듈 임포트 테스트
            try:
                from src.prac_text import ProfanityFilter
                from src.blur import blur
                from src.crop import crop_image
                from src.flip_horizontal import flip_horizontal
                from src.flip_vertical import flip_vertical
                from src.process import wav_del_space
                from src import std_video
                import cv2
            except ImportError as e:
                errors.append(f"[Import Error] {e}. src 폴더 위치를 확인하세요.")
                return errors

            # 1. 텍스트 필터 테스트
            try:
                pf = ProfanityFilter()
                if not pf.has_profanity("씨발"):
                    errors.append("[Text Error] 욕설 감지 실패")
                if "***" not in pf.clean("씨발"):
                    errors.append("[Text Error] 욕설 마스킹 실패")
            except Exception as e:
                errors.append(f"[Text Exception] {e}")

            # 2. 이미지 처리 테스트
            try:
                img = Image.new('RGB', (100, 100), color='red')
                
                # Blur
                if blur(img, ksize=5).size != (100, 100):
                    errors.append("[Image Error] Blur 후 크기 변경됨")
                
                # Flip Horizontal
                pixels = img.load()
                for y in range(100):
                    for x in range(50): pixels[x, y] = (0, 0, 0)
                flipped = flip_horizontal(img)
                if flipped.getpixel((99, 0)) != (0, 0, 0):
                    errors.append("[Image Error] 좌우 반전 실패")

                # Crop
                if crop_image(img, (20, 20, 80, 80)).size != (60, 60):
                    errors.append("[Image Error] 자르기(Crop) 크기 불일치")
            except Exception as e:
                errors.append(f"[Image Exception] {e}")

            # 3. 오디오 처리 테스트
            try:
                sr = 22050
                # 5초 길이 더미 파형 생성 (중간 무음 포함)
                y = np.sin(2 * np.pi * 440 * np.linspace(0, 5, int(sr * 5)))
                y[int(sr):int(sr*3)] = 0
                
                segments = wav_del_space(y, sr)
                if len(segments) < 2:
                    errors.append("[Audio Error] 무음 구간 분할 실패")
            except Exception as e:
                errors.append(f"[Audio Exception] {e}")

            # 4. 비디오 데이터셋 테스트
            test_dir = "temp_test_frames_silent"
            try:
                if not os.path.exists(test_dir):
                    os.makedirs(test_dir)
                
                # 더미 프레임 생성
                for i in range(10):
                    dummy = np.zeros((100, 100, 3), dtype=np.uint8)
                    cv2.imwrite(os.path.join(test_dir, f"frame_{i:06d}.jpg"), dummy)
                
                # 시퀀스 생성 함수 호출
                dataset = std_video.create_sequences(test_dir, 3)
                
                # 10개 프레임 / 시퀀스 길이 3 = 3개 생성 예상
                if len(dataset) != 3:
                    errors.append(f"[Video Error] 데이터셋 생성 개수 오류 (Expected 3, Got {len(dataset)})")
            
            except Exception as e:
                errors.append(f"[Video Exception] {e}")
            finally:
                if os.path.exists(test_dir):
                    shutil.rmtree(test_dir)

        except Exception as e:
            errors.append(f"[System Error] {e}")

    return errors

if __name__ == "__main__":
    found_errors = run_tests()
    for err in found_errors:
        print(err)

    if not found_errors:
        print("Porgram is Successful!!!!") # 베뤼나이스