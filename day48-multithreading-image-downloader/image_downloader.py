"""
Image Downloader with Multithreading
Downloads images from URLs using threading for parallel processing
"""

import os
import time
import threading
import requests
from datetime import datetime
from typing import List, Dict, Any


class ImageDownloader:
    """Multi-threaded image downloader"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
        self.lock = threading.Lock()
        self.start_time = None
        self.end_time = None
    
    def download_image(self, url: str, filename: str = None) -> Dict[str, Any]:
        """
        Download a single image from URL
        
        Args:
            url: Image URL
            filename: Output filename (optional)
        
        Returns:
            Dictionary with download results
        """
        try:
            # Generate filename if not provided
            if filename is None:
                filename = url.split('/')[-1]
                if not filename or '.' not in filename:
                    filename = f"image_{hash(url)}.jpg"
            
            # Ensure images directory exists
            os.makedirs("images", exist_ok=True)
            filepath = f"images/{filename}"
            
            # Download image
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            result = {
                'url': url,
                'filename': filename,
                'filepath': filepath,
                'size': len(response.content),
                'success': True,
                'thread': threading.current_thread().name
            }
            
            print(f"[OK] Downloaded: {filename} ({len(response.content)} bytes) - {threading.current_thread().name}")
            return result
            
        except requests.exceptions.RequestException as e:
            result = {
                'url': url,
                'filename': filename,
                'error': str(e),
                'success': False,
                'thread': threading.current_thread().name
            }
            print(f"[ERROR] Failed to download {filename or url}: {e}")
            return result
    
    def download_images_sequential(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Download images sequentially (no threading)
        
        Args:
            urls: List of image URLs
        
        Returns:
            List of download results
        """
        print("\n" + "="*60)
        print("SEQUENTIAL DOWNLOAD (No Threading)")
        print("="*60)
        
        self.start_time = time.time()
        results = []
        
        for i, url in enumerate(urls):
            filename = f"seq_{i+1}.jpg"
            result = self.download_image(url, filename)
            results.append(result)
        
        self.end_time = time.time()
        self.results = results
        
        return results
    
    def download_images_multithreaded(self, urls: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Download images using multiple threads
        
        Args:
            urls: List of image URLs
            max_workers: Maximum number of threads
        
        Returns:
            List of download results
        """
        print("\n" + "="*60)
        print(f"MULTITHREADED DOWNLOAD (Threads: {max_workers})")
        print("="*60)
        
        self.start_time = time.time()
        
        # Split URLs into chunks for each thread
        chunks = []
        for i in range(0, len(urls), max_workers):
            chunk = urls[i:i+max_workers]
            chunks.append(chunk)
        
        threads = []
        results = []
        
        # Create and start threads
        for chunk_index, chunk in enumerate(chunks):
            thread = threading.Thread(
                target=self._download_chunk,
                args=(chunk, chunk_index, results)
            )
            thread.name = f"Worker-{chunk_index+1}"
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        self.end_time = time.time()
        self.results = results
        
        return results
    
    def _download_chunk(self, urls: List[str], chunk_index: int, results: List):
        """
        Download a chunk of images (called by thread)
        
        Args:
            urls: List of URLs for this chunk
            chunk_index: Index of this chunk
            results: List to collect results
        """
        for i, url in enumerate(urls):
            filename = f"thread_{chunk_index+1}_{i+1}.jpg"
            result = self.download_image(url, filename)
            
            # Thread-safe append to results
            with self.lock:
                results.append(result)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the download operation
        
        Returns:
            Dictionary with statistics
        """
        if not self.results:
            return {"error": "No downloads performed"}
        
        successful = [r for r in self.results if r.get('success', False)]
        failed = [r for r in self.results if not r.get('success', False)]
        
        total_size = sum([r.get('size', 0) for r in successful])
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        return {
            "total_images": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "time_seconds": round(total_time, 2),
            "images_per_second": round(len(successful) / total_time, 2) if total_time > 0 else 0
        }
    
    def compare_performance(self, urls: List[str]) -> Dict[str, Any]:
        """
        Compare sequential vs multithreaded performance
        
        Args:
            urls: List of image URLs
        
        Returns:
            Comparison results
        """
        # Sequential download
        seq_results = self.download_images_sequential(urls[:10])
        seq_stats = self.get_statistics()
        
        time.sleep(2)  # Wait between tests
        
        # Multithreaded download
        mt_results = self.download_images_multithreaded(urls[:10], max_workers=5)
        mt_stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON")
        print("="*60)
        print(f"{'Method':<20} {'Time (s)':>15} {'Images/s':>15} {'Success':>12}")
        print("-"*60)
        print(f"{'Sequential':<20} {seq_stats.get('time_seconds', 0):>15.2f} "
              f"{seq_stats.get('images_per_second', 0):>15.2f} "
              f"{seq_stats.get('successful', 0)}/{seq_stats.get('total_images', 0)}")
        print(f"{'Multithreaded':<20} {mt_stats.get('time_seconds', 0):>15.2f} "
              f"{mt_stats.get('images_per_second', 0):>15.2f} "
              f"{mt_stats.get('successful', 0)}/{mt_stats.get('total_images', 0)}")
        print("="*60 + "\n")
        
        speedup = round(seq_stats.get('time_seconds', 0) / mt_stats.get('time_seconds', 0), 2) if mt_stats.get('time_seconds', 0) > 0 else 0
        print(f"Speedup: {speedup}x faster with multithreading")
        print("="*60 + "\n")
        
        return {
            'sequential': seq_stats,
            'multithreaded': mt_stats,
            'speedup': speedup
        }


def load_urls_from_file(filename: str) -> List[str]:
    """
    Load image URLs from text file
    
    Args:
        filename: Path to text file with URLs
    
    Returns:
        List of URLs
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"[OK] Loaded {len(urls)} URLs from {filename}")
        return urls
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filename}")
        return []