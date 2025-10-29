# services/gemini_service.py
import google.generativeai as genai
import os
import uuid
import matplotlib.pyplot as plt
import seaborn as sns

genai.configure(api_key="AIzaSyAN7MzgqQ9xcmic1oTdhgsYfWhoSMa19Yk")
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_visualization_code(df, task_description, output_dir="visuals"):
    """
    Generates and executes visualization code using Gemini, 
    saving the generated charts into the visuals folder.
    """
    os.makedirs(output_dir, exist_ok=True)

    # ✅ Unique filename in the visuals folder
    filename = f"plot_{uuid.uuid4().hex}.png"
    output_path = os.path.join(output_dir, filename)

    # --- Build Gemini prompt ---
    prompt = f"""
    You are a Python data visualization expert.
    Given this dataset with columns: {list(df.columns)} 
    and sample data: {df.head(5).to_dict()},
    write matplotlib/seaborn code to {task_description}.
    Use variable df (already loaded), plt, and sns.
    Save the figure as '{output_path}' and close it.
    Only output the code, no explanation.
    """

    # --- Generate code ---
    response = model.generate_content(prompt)
    code = response.text.strip("```python").strip("```")

    # --- Ensure plt.savefig and plt.close are always used ---
    if "plt.savefig" not in code:
        code += f"\nplt.savefig(r'{output_path}')\nplt.close()"
    else:
        # Replace any relative paths to the correct visuals folder
        code = code.replace("plt.savefig(", f"plt.savefig(r'{output_path}')\nplt.close();#")

    # --- Safe local context ---
    local_vars = {"df": df, "plt": plt, "sns": sns}

    try:
        exec(code, {}, local_vars)
    except Exception as e:
        print("⚠️ Error executing Gemini-generated code:", e)
        print("Generated Code:\n", code)
        return None

    return output_path
