from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel 
import torch
from transformers import CLIPModel,CLIPProcessor
from typing import Optional
import torchvision.transforms as transforms
import uvicorn
import pickle
from PIL import Image
import requests

MODEL_NAME = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
CLASSIFIER_FILENAME = "model.sav"
THRESHOLDS = [5.06, 3.96, 5.38, 4.74, 4.31, 5.31, 4.98]
app = FastAPI()

class CLIPSolution:
    def __init__(self):

        self.model = CLIPModel.from_pretrained(MODEL_NAME)
        self.processor = CLIPProcessor.from_pretrained(MODEL_NAME)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.classifier = pickle.load(open(CLASSIFIER_FILENAME, 'rb'))

    @torch.no_grad()
    def get_text_features(self, text):
        inputs = self.processor(text=text, return_tensors="pt")
        inputs = inputs.to(self.device)
        text_features = self.model.get_text_features(**inputs)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_features = text_features.tolist()
        return text_features

    @torch.no_grad()
    def get_image_features(self, images):
        inputs = self.processor(images=images, return_tensors="pt")
        inputs = inputs.to(self.device)
        image_features = self.model.get_image_features(**inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        image_features = image_features.detach().cpu().numpy()
        return image_features

    def predict(self, image_features):

        logits = self.classifier.decision_function(image_features)

        for label in range(7):
            if logits[0][label] >= THRESHOLDS[label]:
                return 0
        return 1


processor = CLIPSolution()


class URL(BaseModel):
    url: str
    url_list: Optional[list]

@app.post("/predict")
def read_item(body: URL):
    
    try :

        image = Image.open(requests.get(body.url, stream=True).raw)

        transform = transforms.Compose([transforms.PILToTensor()])

        torch_image = transform(image)

        feature = processor.get_image_features(torch_image)

        prediction = processor.predict(feature)

        return {"success": True, "label": prediction, "embedding": feature.tolist()}
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={"success": False, "details": "Error Occured"})


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8789)