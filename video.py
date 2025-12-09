import os
import sys

# src 폴더를 모듈 경로로 인식하기 위해 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src import std_video, videowriter, video_blur

def main():
    # ========================================================
    # 경로 설정 (src/data 구조)
    # ========================================================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "src", "data")
    
    # 입력 파일: src/data/input/video.mp4
    INPUT_VIDEO = os.path.join(DATA_DIR, "input", "video.mp4")
    
    # 1단계 결과물: 프레임 폴더 & npy 파일
    FRAMES_DIR = os.path.join(DATA_DIR, "output" ,"standardized_frames_16x9")
    DATASET_NPY = os.path.join(DATA_DIR, "output", "video_dataset_16x9.npy")
    
    # 2단계 결과물: 중간 mp4 파일
    STEP2_VIDEO = os.path.join(DATA_DIR, "output", "final_output.mp4")
    
    # 3단계 결과물: 최종 블러링 된 mp4 파일
    STEP3_VIDEO = os.path.join(DATA_DIR, "output", "output_blur.mp4")

    # ========================================================
    # 실행
    # ========================================================
    
    print("\n========== [Step 1] 프레임 추출 및 데이터셋 생성 ==========")
    std_video.run(INPUT_VIDEO, FRAMES_DIR, DATASET_NPY)
    
    print("\n========== [Step 2] 영상 변환 (프레임 -> MP4) ==========")
    videowriter.run(FRAMES_DIR, STEP2_VIDEO)
    
    print("\n========== [Step 3] 얼굴 인식 및 블러 처리 ==========")
    video_blur.run(STEP2_VIDEO, STEP3_VIDEO)

    print("\n모든 작업이 완료되었습니다!")

if __name__ == "__main__":
    main()