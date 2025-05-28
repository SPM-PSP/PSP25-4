import os
import argparse
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from local_infer import FastDetectGPT

app = FastAPI(title="Fast-DetectGPT API")

# 全局模型加载
DETECTOR = None

class DetectRequest(BaseModel):
    text: str
    sampling_model: str = "falcon-7b"
    scoring_model: str = "falcon-7b-instruct"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

class DetectResponse(BaseModel):
    score: float
    is_ai_generated: bool
    tokens_processed: int

@app.on_event("startup")
def load_model():
    """启动时加载模型（避免每次请求重复加载）"""
    global DETECTOR
    args = argparse.Namespace(
        sampling_model_name=os.getenv("SAMPLING_MODEL", "falcon-7b"),
        scoring_model_name=os.getenv("SCORING_MODEL", "falcon-7b-instruct"),
        device=os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu"),
        cache_dir=os.getenv("CACHE_DIR", "/autodl_tmp/cache")
    )
    DETECTOR = FastDetectGPT(args)

@app.post("/detect", response_model=DetectResponse)
async def detect(request: DetectRequest):
    """处理文本检测请求"""
    if not DETECTOR:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        prob, crit, ntokens = DETECTOR.compute_prob(request.text)
        return {
            "prob": float(prob),
            "crit": float(crit),
            "tokens_processed": ntokens
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,  # 多GPU可增加workers
        timeout_keep_alive=60
    )