import google.generativeai as genai
import os
import uuid

genai.configure(api_key="AIzaSyAN7MzgqQ9xcmic1oTdhgsYfWhoSMa19Yk")
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_visualization_code(df, task_description, output_dir="visuals"):
    prompt = f"""
    You are a Python data visualization expert.
    Given this dataset with columns: {list(df.columns)} 
    and sample data: {df.head(5).to_dict()}
    Write matplotlib/seaborn code to {task_description}.
    Use variable df (already loaded), plt, and sns.
    Instead of plt.show(), save the plot as a PNG file using plt.savefig('output_path'), then close the plot with plt.close().
    Only output the code, no explanation.
    """

    response = model.generate_content(prompt)
    code = response.text.strip("```python").strip("```")

    # Generate a unique filename for the plot
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"plot_{uuid.uuid4().hex}.png")

    # Replace plt.show() with plt.savefig and plt.close()
    code = code.replace("plt.show()", f"plt.savefig(r'{output_path}')\nplt.close()")

    # Prepare the local namespace for exec
    local_vars = {"df": df}
    import matplotlib.pyplot as plt
    import seaborn as sns
    local_vars["plt"] = plt
    local_vars["sns"] = sns

    # Execute the generated code
    exec(code, {}, local_vars)

    return output_path