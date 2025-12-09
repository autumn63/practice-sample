import cv2
import numpy as np
import os
import glob

# =================================================================
# 1. 영상 표준화, 프레임 추출, 저장
# =================================================================

def standardize_and_extract_frames(video_path, output_dir, target_size, interval, clip_limit, tile_grid_size):
    """
    동영상을 읽어 해상도(16:9), 밝기/대비, 색감 표준화하여 프레임을 저장
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    frame_num = 0
    saved_count = 0
    
    # CLAHE 객체 생성 (밝기/대비 균일화 도구)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    print("--- 1단계: 영상 표준화 및 프레임 추출 시작 (16:9 비율 적용) ---")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        if frame_num % interval == 0:
            
            # 1. 해상도 맞추기 (크기 조정 Resizing)
            resized_frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)

            # 2. 밝기 및 대비 균일화 (CLAHE 적용)
            lab = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            contrast_enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            # 3. 색감 정규화 (Normalization)
            normalized_frame = contrast_enhanced_frame.astype(np.float32) / 255.0

            # --- 저장용: 0-255 범위로 다시 변환 ---
            frame_to_save = (normalized_frame * 255).astype(np.uint8)

            # 4. 프레임 파일로 저장
            frame_filename = os.path.join(output_dir, f'frame_{frame_num:06d}.jpg')
            cv2.imwrite(frame_filename, frame_to_save)
            
            saved_count += 1
            
        frame_num += 1

    cap.release()
    print(f"1단계 완료: 총 {frame_num} 프레임 중 {saved_count}개 표준화된 프레임이 저장됨.")
    return saved_count


# =================================================================
# 2. 저장된 프레임들을 시퀀스 데이터셋으로 구성 및 저장
# =================================================================

def create_sequences(frame_directory, sequence_length):
    """
    저장된 개별 프레임들을 불러와 시퀀스 배열(Numpy)로 구성
    """
    frame_files = sorted(glob.glob(os.path.join(frame_directory, '*.jpg')))
    
    if len(frame_files) < sequence_length:
        print("경고: 시퀀스 구성에 필요한 프레임 수가 부족합니다.")
        return np.array([])

    all_frames = []
    
    # 3-1. 저장된 모든 프레임 불러오기
    for file_path in frame_files:
        frame = cv2.imread(file_path, cv2.IMREAD_COLOR) 
        frame = frame.astype(np.float32) / 255.0
        all_frames.append(frame)

    all_frames = np.array(all_frames)

    # 3-2. 시퀀스 생성 (오버랩 없음)
    sequences = []
    num_sequences = len(all_frames) // sequence_length
    
    for i in range(num_sequences):
        start_idx = i * sequence_length
        end_idx = start_idx + sequence_length
        
        sequence = all_frames[start_idx:end_idx]
        sequences.append(sequence)

    return np.array(sequences)

# =================================================================
# 3. 실행 함수 (모듈화)
# =================================================================
def run(INPUT_VIDEO_PATH, PROCESSED_DIR, DATASET_OUTPUT_PATH):
    # --- 사용자 설정 영역 (변수명 유지) ---
    TARGET_ASPECT_RATIO = (16, 9)
    TARGET_SIZE = (320, 180)
    SEQUENCE_LENGTH = 30
    FRAME_INTERVAL = 5
    CLIP_LIMIT = 2.0
    TILE_GRID_SIZE = (8, 8)
    
    # 1단계 실행
    saved_frames_count = standardize_and_extract_frames(
        INPUT_VIDEO_PATH,
        PROCESSED_DIR,
        TARGET_SIZE,
        FRAME_INTERVAL,
        CLIP_LIMIT,
        TILE_GRID_SIZE
    )

    if saved_frames_count > 0:
        print("--- 2단계: 시퀀스 데이터셋 구성 및 저장 시작 ---")

        # 2단계 실행
        video_dataset = create_sequences(
            frame_directory=PROCESSED_DIR,
            sequence_length=SEQUENCE_LENGTH
        )

        # 결과 확인 및 저장
        if video_dataset.size > 0:
            print(f"데이터셋 형태 (Shape): {video_dataset.shape}")
            
            # 경로가 없으면 생성
            os.makedirs(os.path.dirname(DATASET_OUTPUT_PATH), exist_ok=True)
            np.save(DATASET_OUTPUT_PATH, video_dataset)
            print(f"최종 데이터셋이 '{DATASET_OUTPUT_PATH}' 파일로 저장되었습니다.")