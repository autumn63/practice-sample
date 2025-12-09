# All-in-One Media Processing Library

Python-based open-source library for processing **Image, Video, Audio, and Text**.  
This project provides a comprehensive toolkit for multimedia data preprocessing, designed for AI/ML pipelines and content creation.

## Features

| Module | Features |
| :--- | :--- |
| **Image** | Blur, Crop (Drag & Drop), Flip (Horizontal/Vertical), Undo/Redo Support |
| **Video** | Frame Extraction (16:9), Standardization (CLAHE), Face Blurring (MediaPipe) |
| **Audio** | Video-to-Wav Conversion, Silence Removal, Segmentation, Waveform Visualization |
| **Text** | Profanity Filtering, Text Normalization, Privacy Masking |

---

## Installation

### Prerequisites
- Python 3.8+
- [Anaconda](https://www.anaconda.com/) (Recommended)

### Dependencies
Install the required packages:

```bash
pip install opencv-python numpy pillow moviepy librosa matplotlib mediapipe soundfile
```

Note : For macOS,, enshure ```tk``` is installed via conda to prevent GUI crashes.
```bash
conda install -c conda-forge tk
```

## Usage
### 1.Image Tool(GUI)

A Thkinter-based GUI tool for image editing
```Bash
python image.py
```
- Open Image: Load any image file
- Blur: Apply Gaussian blur to the entiee image or selected area.
- Crop: Drag and drop to crop regions
- Flip: Flip image horizontally or vertically.

### 2.Video Processing Pipeline

Processes video files for dataset creation.
```bash
python video.py
```
- Step 1: Std frames n extract to ```scr/data/standardized_frames_16x9```.
- Step 2: Conver frames back to MP4.
- Step 3: Detect faces and apply blur for priacy.

### 3.Audio Processing

Extracts audio from video and removes silence.
```bash
python audio.py
```
- Extracts audio from ```src/data/input/video.mp4```.
- Removes silent intervals automatically.
- Saves segmented audio files to ```src/data/output```.

### 4.Text Filterrig

Filters profanity and normalizes text.
```bash
python text.py
```

## Testing
We provide a comprehensive unit test  suite to verify all modules.
```bash
python test_suite.py
```
if all test pass, you will see Goal Msg without errors.

## License
Distrivute under the MIT license. See ```LICENSE``` for more info.
