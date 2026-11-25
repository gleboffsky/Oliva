# Oliva

Desktop tool for **batch image processing**: removes the background, crops
images and writes a CSV report.

## Features

- Pick a source folder and an output CSV
- Background removal (`rembg`), cropping and filtering (`Pillow`)
- Batch processing with progress
- Error log: `%USERPROFILE%\Documents\Oliva_errors.txt`

## Stack

Python 3, PyQt5, Pillow, numpy, rembg.

## Run

```bash
pip install PyQt5 Pillow numpy rembg
python Oliva.py
```
