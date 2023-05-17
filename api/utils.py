from mlflow import MlflowClient
import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='secret.json'
client = MlflowClient("http://34.143.177.166:5000/", "http://34.143.177.166:5000/")

CLIP_RUN_ID = "d359f45f1f934eb8b8eb197d42f4a556"
CLIP_REMOTE_ARTIFACT_PATH = "clip-laion"
LR_RUN_ID = "e27fbc7c24bf4642be1ea89e4bc04b6b"
LR_REMOTE_ARTIFACT_PATH = "lr-weight"
LOCAL_DIR = "."

THRESHOLDS = [5.059999999999594,
 3.959999999999617,
 5.379999999999587,
 4.7399999999996005,
 4.3099999999996115,
 5.30999999999959,
 4.979999999999595]

def download_weight():
    
    # download model weight from mlflow
    print("Downloading model weight...")
    if not os.path.exists(CLIP_REMOTE_ARTIFACT_PATH):
        clip_path = client.download_artifacts(CLIP_RUN_ID, CLIP_REMOTE_ARTIFACT_PATH, LOCAL_DIR)
    if not os.path.exists(LR_REMOTE_ARTIFACT_PATH):
        lr_path = client.download_artifacts(LR_RUN_ID, LR_REMOTE_ARTIFACT_PATH, LOCAL_DIR)
    print("Finish downloading model weight.")
