from fastapi import APIRouter, Form
import pandas as pd
from services.gemini_service import generate_visualization_code
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

router = APIRouter()

@router.post("/auto")
async def auto_visualize(file_path: str = Form(...)):
    df = pd.read_csv(file_path)
    code = generate_visualization_code(df, "Create 5 random interesting charts.")
    return {"generated_code": code}

@router.post("/chat")
async def chat_visualize(file_path: str = Form(...), query: str = Form(...)):
    df = pd.read_csv(file_path)
    code = generate_visualization_code(df, query)

    # Execute code and convert plot to base64
    buffer = io.BytesIO()
    try:
        exec(code, {"df": df, "plt": plt, "sns": sns})
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        return {"generated_code": code, "chart": image_base64}
    except Exception as e:
        return {"error": str(e), "generated_code": code}
