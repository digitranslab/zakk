#!/usr/bin/env python3
"""
Script to download all required models for the Zakk model server.
"""

import os
import shutil
from transformers import AutoTokenizer
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer


def download_models():
    """Download all required models."""
    print("=== Starting model downloads ===")
    
    # Download tokenizers
    print("Downloading tokenizers...")
    AutoTokenizer.from_pretrained('distilbert-base-uncased')
    AutoTokenizer.from_pretrained('mixedbread-ai/mxbai-rerank-xsmall-v1')
    print("Tokenizers downloaded successfully")
    
    # Download digitranslab models
    print("Downloading digitranslab models...")
    
    try:
        snapshot_download('digitranslab/hybrid-intent-token-classifier', local_files_only=False)
        print("Successfully cached hybrid-intent-token-classifier")
    except Exception as e:
        print(f"hybrid-intent-token-classifier not available, will use fallback: {e}")
    
    try:
        snapshot_download('digitranslab/information-content-model', local_files_only=False)
        print("Successfully cached information-content-model")
    except Exception as e:
        print(f"information-content-model not available, will use fallback: {e}")
    
    # Download other models
    print("Downloading other models...")
    snapshot_download('nomic-ai/nomic-embed-text-v1')
    snapshot_download('mixedbread-ai/mxbai-rerank-xsmall-v1')
    
    # Load sentence transformer
    SentenceTransformer(model_name_or_path='nomic-ai/nomic-embed-text-v1', trust_remote_code=True)
    print("All models downloaded successfully")
    
    # Clean up any temporary files
    cache_dir = '/root/.cache/huggingface'
    if os.path.exists(cache_dir):
        for item in os.listdir(cache_dir):
            item_path = os.path.join(cache_dir, item)
            if os.path.isdir(item_path) and item.startswith('tmp'):
                shutil.rmtree(item_path)
                print(f"Cleaned up temporary directory: {item}")
    
    print("Cleanup completed")
    print("=== Model downloads finished ===")


if __name__ == "__main__":
    download_models() 