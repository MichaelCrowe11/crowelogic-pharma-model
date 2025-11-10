#!/usr/bin/env python3
"""
Cloud Results Collector
Download batch results from cloud storage (S3/GCS) and combine them

Usage:
    # Collect from AWS S3
    python collect_cloud_results.py --provider aws --bucket your-pharma-bucket

    # Collect from GCP Cloud Storage
    python collect_cloud_results.py --provider gcp --bucket your-pharma-bucket

    # Collect and auto-combine
    python collect_cloud_results.py --provider aws --bucket your-pharma-bucket --combine

    # Monitor deployment progress
    python collect_cloud_results.py --provider aws --bucket your-pharma-bucket --monitor
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class CloudResultsCollector:
    """Collect batch results from cloud storage"""

    def __init__(self, provider: str, bucket: str):
        self.provider = provider.lower()
        self.bucket = bucket
        self.local_dir = Path("collected_batches")
        self.local_dir.mkdir(exist_ok=True)

    def download_from_s3(self, prefix: str = "batches/"):
        """Download results from AWS S3"""
        print(f"\n{'='*70}")
        print(f"Downloading from S3: s3://{self.bucket}/{prefix}")
        print(f"{'='*70}\n")

        cmd = [
            "aws", "s3", "sync",
            f"s3://{self.bucket}/{prefix}",
            str(self.local_dir),
            "--exclude", "*",
            "--include", "batch_*.jsonl",
            "--include", "batch_*_stats.json"
        ]

        print(f"Running: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"\n✓ Download complete → {self.local_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error downloading from S3: {e}")
            print(e.stderr)
            return False

    def download_from_gcs(self, prefix: str = "batches/"):
        """Download results from GCP Cloud Storage"""
        print(f"\n{'='*70}")
        print(f"Downloading from GCS: gs://{self.bucket}/{prefix}")
        print(f"{'='*70}\n")

        cmd = [
            "gsutil", "-m", "cp",
            f"gs://{self.bucket}/{prefix}batch_*.jsonl",
            f"gs://{self.bucket}/{prefix}batch_*_stats.json",
            str(self.local_dir)
        ]

        print(f"Running: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
            print(f"\n✓ Download complete → {self.local_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error downloading from GCS: {e}")
            print(e.stderr)
            return False

    def download(self, prefix: str = "batches/"):
        """Download results based on provider"""
        if self.provider == "aws":
            return self.download_from_s3(prefix)
        elif self.provider == "gcp":
            return self.download_from_gcs(prefix)
        else:
            print(f"Unsupported provider: {self.provider}")
            return False

    def list_batches(self) -> List[Dict]:
        """List downloaded batches with stats"""
        batches = []

        batch_files = sorted(self.local_dir.glob("batch_*.jsonl"))

        print(f"\n{'='*70}")
        print(f"DOWNLOADED BATCHES ({len(batch_files)} found)")
        print(f"{'='*70}\n")

        for batch_file in batch_files:
            batch_id = batch_file.stem.replace("batch_", "")
            stats_file = self.local_dir / f"batch_{batch_id}_stats.json"

            # Load stats
            stats = {}
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    stats = json.load(f)

            # Count examples
            with open(batch_file, 'r') as f:
                num_examples = sum(1 for _ in f)

            batch_info = {
                "batch_id": batch_id,
                "file": batch_file,
                "num_examples": num_examples,
                "stats": stats
            }
            batches.append(batch_info)

            # Print summary
            compounds = stats.get('compounds_fetched', 'N/A')
            errors = stats.get('errors', 'N/A')
            duration = stats.get('duration_seconds', 0)

            print(f"Batch {batch_id}:")
            print(f"  Examples: {num_examples:,}")
            print(f"  Compounds: {compounds}")
            print(f"  Errors: {errors}")
            print(f"  Duration: {duration/60:.1f} min")
            print()

        return batches

    def monitor_cloud_storage(self, check_interval: int = 60):
        """Monitor cloud storage for new batches"""
        print(f"\n{'='*70}")
        print("MONITORING CLOUD STORAGE")
        print(f"Provider: {self.provider}")
        print(f"Bucket: {self.bucket}")
        print(f"Check interval: {check_interval}s")
        print(f"{'='*70}\n")

        last_count = 0

        while True:
            try:
                # List files in cloud storage
                if self.provider == "aws":
                    cmd = ["aws", "s3", "ls", f"s3://{self.bucket}/batches/", "--recursive"]
                elif self.provider == "gcp":
                    cmd = ["gsutil", "ls", f"gs://{self.bucket}/batches/**"]
                else:
                    print(f"Unsupported provider: {self.provider}")
                    return

                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                files = [line for line in result.stdout.split('\n') if 'batch_' in line and '.jsonl' in line]
                current_count = len(files)

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Found {current_count} batch files", end='')

                if current_count > last_count:
                    new_batches = current_count - last_count
                    print(f" (+{new_batches} new!)")
                    last_count = current_count
                else:
                    print()

                time.sleep(check_interval)

            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break
            except Exception as e:
                print(f"Error monitoring: {e}")
                time.sleep(check_interval)

    def combine_batches(self):
        """Combine downloaded batches"""
        print(f"\n{'='*70}")
        print("COMBINING BATCHES")
        print(f"{'='*70}\n")

        cmd = [
            "python3", "combine_batches.py",
            "--input-dir", str(self.local_dir),
            "--output", "cloud_combined_dataset.jsonl",
            "--split",
            "--deduplicate"
        ]

        print(f"Running: {' '.join(cmd)}\n")

        try:
            subprocess.run(cmd, check=True)
            print(f"\n✓ Batches combined successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error combining batches: {e}")


def main():
    parser = argparse.ArgumentParser(description='Collect batch results from cloud storage')
    parser.add_argument('--provider', choices=['aws', 'gcp'], required=True,
                       help='Cloud storage provider')
    parser.add_argument('--bucket', type=str, required=True,
                       help='Storage bucket name')
    parser.add_argument('--prefix', type=str, default='batches/',
                       help='Prefix/path in bucket (default: batches/)')
    parser.add_argument('--download', action='store_true', default=True,
                       help='Download batch files (default: True)')
    parser.add_argument('--combine', action='store_true',
                       help='Combine batches after download')
    parser.add_argument('--monitor', action='store_true',
                       help='Monitor cloud storage for new batches')
    parser.add_argument('--check-interval', type=int, default=60,
                       help='Monitoring check interval in seconds (default: 60)')

    args = parser.parse_args()

    collector = CloudResultsCollector(provider=args.provider, bucket=args.bucket)

    if args.monitor:
        collector.monitor_cloud_storage(check_interval=args.check_interval)
    else:
        if args.download:
            success = collector.download(prefix=args.prefix)
            if not success:
                print("Download failed. Exiting.")
                sys.exit(1)

        # List batches
        batches = collector.list_batches()

        if args.combine and batches:
            collector.combine_batches()


if __name__ == "__main__":
    main()
