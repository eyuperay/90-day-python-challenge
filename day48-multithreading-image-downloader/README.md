# Day 48 - Multithreading Image Downloader

## About This Project
This project demonstrates multithreading in Python by downloading images from URLs simultaneously. It compares sequential vs multithreaded performance.

## Features
- Download multiple images from URLs
- Sequential and multithreaded modes
- Performance comparison
- Thread-safe operations
- Error handling

## Usage

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the program
python main.py

### 3. Select download method
- 1: Sequential (no threading)
- 2: Multithreaded (fast)
- 3: Compare performance

## Image Sources
Images are downloaded from picsum.photos - free placeholder images:
- https://picsum.photos/200/300?random=1

## Threading Concepts Demonstrated
- Creating and starting threads
- Thread synchronization with locks
- Thread-safe data collection
- Performance comparison

## Learning Objectives
- Understanding multithreading in Python
- Parallel vs sequential execution
- Thread safety
- Performance optimization
- Real-world application of threading

## Performance Benefits
Multithreading significantly speeds up I/O-bound operations like downloading images, as the program can download multiple images simultaneously while waiting for network responses.