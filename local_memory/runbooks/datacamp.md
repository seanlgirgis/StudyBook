# DataCamp Video Screenshot Extraction

## PySceneDetect For Lesson Videos

Perfect — it is working correctly.

For a DataCamp lesson video, start with:

```powershell
python -m scenedetect `
  -i ".\lesson.mp4" `
  -o ".\screenshots" `
  detect-content `
  save-images
```

That will detect scene changes and save representative images into `screenshots`.

A slightly better version for slide-heavy course videos is:

```powershell
python -m scenedetect `
  -i ".\lesson.mp4" `
  -o ".\screenshots" `
  -m 2s `
  detect-content --threshold 22 `
  save-images --num-images 1
```

What those options do:

* `-m 2s` prevents extremely short scenes.
* `--threshold 22` controls sensitivity. Lower detects more changes; higher detects fewer.
* `--num-images 1` saves one representative screenshot per scene instead of several.

For your workflow, I recommend first trying:

```powershell
python -m scenedetect -i ".\lesson.mp4" -o ".\screenshots" -m 2s detect-content --threshold 22 save-images --num-images 1
```

If it creates too many screenshots, raise the threshold:

```powershell
--threshold 27
```

If it misses important slide changes, lower it:

```powershell
--threshold 18
```

For multiple videos in one chapter folder:

```powershell
Get-ChildItem -Filter *.mp4 | ForEach-Object {
    $output = Join-Path $_.DirectoryName ($_.BaseName + "_screenshots")

    python -m scenedetect `
        -i $_.FullName `
        -o $output `
        -m 2s `
        detect-content --threshold 22 `
        save-images --num-images 1
}
```

That creates a separate screenshot folder for each video.

## Example Successful Run

```powershell
PS D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design\source_material\Chapter1> python -m scenedetect -i ".\OLTP and OLAP.mp4"  -o ".\screenshots" detect-content   save-images
[PySceneDetect] PySceneDetect 0.7
[PySceneDetect] Detecting scenes...
  Detected: 1 | Progress: 100%|███████████████████████████████████████████████| 8533/8533 [00:15<00:00, 560.14frames/s]
[PySceneDetect] Processed 8533 frames in 15.3 seconds (average 559.15 FPS).
[PySceneDetect] Detected 2 scenes, average shot length 142.2 seconds.
[PySceneDetect] Saving 3 images per scene [format=jpg] D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design\source_material\Chapter1\screenshots
100%|████████████████████████████████████████████████████████████████████████████████| 6/6 [00:00<00:00, 35.56images/s]
PS D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design\source_material\Chapter1>
```

## extract_slide_frames.py For Final Slide Frames

Script path currently in use:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\database_design\source_material\Chapter1\extract_slide_frames.py
```

Purpose:

Use this Python utility to extract interval screenshots from a course MP4 and keep the last frame from each slide/build sequence.

Requirements:

```powershell
pip install pillow numpy
```

FFmpeg must be available on the Windows `PATH`.

Basic command from the chapter folder:

```powershell
python ".\extract_slide_frames.py" ".\Storing data.mp4"
```

High-frequency capture command used for gradual slide builds:

```powershell
python ".\extract_slide_frames.py" ".\Storing data.mp4" --seconds 0.5
```

What the script does:

1. Accepts an MP4 path or an existing screenshot directory with `--screenshots`.
2. Runs FFmpeg internally when a video path is provided.
3. Writes raw interval screenshots to `interval_screenshots`.
4. Compares consecutive images in grayscale.
5. Starts a new slide group when changed pixels exceed `--change-ratio`.
6. Keeps the last frame from each detected group.
7. Writes selected images to `selected_slide_frames`.
8. Also writes `comparison_report.csv` and `contact_sheet.jpg` in `selected_slide_frames`.

Current defaults from the script:

```text
--seconds 3.0
--change-ratio 0.04
--pixel-delta 18
--overwrite disabled by default
```

Overwrite behavior:

Use `--overwrite` to allow FFmpeg to overwrite existing interval screenshots.

```powershell
python ".\extract_slide_frames.py" ".\Storing data.mp4" --seconds 0.5 --overwrite
```

Existing screenshot mode:

```powershell
python ".\extract_slide_frames.py" --screenshots ".\interval_screenshots"
```

Observed successful run for `Storing data.mp4`:

```text
Input screenshots: 551
Selected slide frames: 13
```

Concise recall answer:

```powershell
python ".\extract_slide_frames.py" ".\Storing data.mp4" --seconds 0.5
```

This runs FFmpeg internally, writes raw frames to `interval_screenshots`, and writes reduced final-slide candidates to `selected_slide_frames`.
