# =================================================================
# 1. 라이브러리 및 설정
# =================================================================

import cv2
import glob
import os

def run(INPUT_DIR, OUTPUT_VIDEO_NAME):
    # --- 사용자 설정 영역 (변수명 유지) ---
    TARGET_FPS = 15.0                            

    # =================================================================
    # 2. 비디오 라이터(VideoWriter) 설정
    # =================================================================

    frame_files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.jpg')))

    if not frame_files:
        print(f"Error: 폴더 '{INPUT_DIR}'에 저장된 이미지 파일이 없습니다.")
        return # exit() 대신 return 사용

    first_frame = cv2.imread(frame_files[0], cv2.IMREAD_COLOR) 
    height, width = first_frame.shape[:2]

    # ⭐ XVID 코덱 사용: MP4 컨테이너에 XVID를 넣어 안정성을 확보하려는 시도 ⭐
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 호환성을 위해 mp4v 권장 (원본은 XVID였으나 Mac등에서 이슈 가능성 있음, 원본 유지 원하시면 XVID로 변경 가능)

    # 출력 폴더 생성
    os.makedirs(os.path.dirname(OUTPUT_VIDEO_NAME), exist_ok=True)

    out = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, TARGET_FPS, (width, height), isColor=True)

    print(f"--- {len(frame_files)}개의 프레임을 MP4 영상으로 변환 시작 (XVID 코덱 시도) ---")

    # =================================================================
    # 3. 프레임 읽고 영상으로 쓰기
    # =================================================================

    for i, file_path in enumerate(frame_files):
        # 컬러 이미지로 읽기 (IMREAD_COLOR)
        frame = cv2.imread(file_path, cv2.IMREAD_COLOR) 
        out.write(frame) 
        
    out.release()
    print("--- 영상 변환 완료 ---")
    print(f"최종 MP4 영상 파일이 '{OUTPUT_VIDEO_NAME}'으로 저장되었습니다.")