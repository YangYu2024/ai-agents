#!/usr/bin/env python3
"""
Quick Model Warmup Script - Run this before using agents for faster responses

Usage: python3 warmup_model.py
"""

import subprocess
import sys
import os

# Run the warmup shell script which handles virtual environment setup
warmup_script = os.path.join(os.path.dirname(__file__), 'scripts', 'warmup.sh')

if __name__ == "__main__":
    try:
        result = subprocess.run(['bash', warmup_script], check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("❌ Error: warmup.sh script not found")
        sys.exit(1)