#!/usr/bin/env python3
"""
Day 48 - Multithreading Image Downloader
Download images using sequential and multithreaded approaches
"""

import os
import time
from image_downloader import ImageDownloader, load_urls_from_file


def main():
    print("=" * 60)
    print("DAY 48 - MULTITHREADING IMAGE DOWNLOADER")
    print("=" * 60 + "\n")
    
    # Load URLs from file
    urls = load_urls_from_file("data/image_urls.txt")
    
    if not urls:
        print("No URLs found. Creating sample URLs...")
        urls = [
            f"https://picsum.photos/200/300?random={i}" 
            for i in range(1, 21)
        ]
        print(f"Generated {len(urls)} sample URLs")
    
    print(f"Total images to download: {len(urls)}")
    
    # Initialize downloader
    downloader = ImageDownloader()
    
    # Ask user for method
    print("\n" + "="*60)
    print("SELECT DOWNLOAD METHOD")
    print("="*60)
    print("1. Sequential (No threading)")
    print("2. Multithreaded (Fast)")
    print("3. Compare Performance (Recommended)")
    print("="*60)
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        # Sequential download
        print("\n" + "="*60)
        print("SEQUENTIAL DOWNLOAD SELECTED")
        print("="*60)
        
        results = downloader.download_images_sequential(urls[:10])
        stats = downloader.get_statistics()
        
        print(f"\n[OK] Downloaded {stats['successful']} images in {stats['time_seconds']:.2f} seconds")
        
    elif choice == "2":
        # Multithreaded download
        print("\n" + "="*60)
        print("MULTITHREADED DOWNLOAD SELECTED")
        print("="*60)
        
        max_workers = input("Number of threads (default: 5): ").strip()
        try:
            max_workers = int(max_workers) if max_workers else 5
        except ValueError:
            max_workers = 5
        
        results = downloader.download_images_multithreaded(urls[:15], max_workers)
        stats = downloader.get_statistics()
        
        print(f"\n[OK] Downloaded {stats['successful']} images in {stats['time_seconds']:.2f} seconds")
        print(f"[OK] Speed: {stats['images_per_second']:.2f} images/second")
        
    else:
        # Performance comparison
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON SELECTED")
        print("="*60)
        print("Downloading 10 images with both methods...\n")
        
        comparison = downloader.compare_performance(urls)
        
        stats = downloader.get_statistics()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    # Count downloaded images
    try:
        images = os.listdir("images")
        print(f"Total images in 'images' folder: {len(images)}")
        
        # Show sample of downloaded images
        if images:
            print("\nSample of downloaded images:")
            for img in images[:5]:
                print(f"  - {img}")
            if len(images) > 5:
                print(f"  ... and {len(images) - 5} more")
    except FileNotFoundError:
        print("No images downloaded yet")
    
    print("\n" + "="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'images' folder for downloaded files")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()