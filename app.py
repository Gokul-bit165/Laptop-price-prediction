import pandas as pd
import joblib
import gradio as gr

try:
    df = pd.read_csv('dataset/cleaned_data.csv')
    model = joblib.load('laptop_price_model.pkl')
except FileNotFoundError:
    print("Please make sure 'cleaned_data.csv' and 'laptop_price_model.pkl' are in the same directory.")
    exit()

brand_options = sorted(df['brand'].unique().tolist())
name_options = sorted(df['name'].unique().tolist())
processor_options = sorted(df['processor'].unique().tolist())
cpu_options = sorted(df['CPU'].unique().tolist())
ram_type_options = sorted(df['Ram_type'].unique().tolist())
rom_type_options = sorted(df['ROM_type'].unique())
gpu_options = sorted(df['GPU'].unique().tolist())
os_options = sorted(df['OS'].unique().tolist())


def predict_price(brand, name, spec_rating, processor, CPU, Ram, Ram_type, ROM, ROM_type, GPU, display_size, resolution_width, resolution_height, OS, warranty):
    input_df = pd.DataFrame([[brand, name, spec_rating, processor, CPU, Ram, Ram_type, ROM, ROM_type, GPU, display_size, resolution_width, resolution_height, OS, warranty]],
                            columns=['brand', 'name', 'spec_rating', 'processor', 'CPU', 'Ram', 'Ram_type', 'ROM', 'ROM_type', 'GPU', 'display_size', 'resolution_width', 'resolution_height', 'OS', 'warranty'])
    predicted_price = model.predict(input_df)[0]
    return f'💰 Predicted Price: ₹{predicted_price:,.2f}'


custom_css = """
#title {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}
.gr-button {
    background: linear-gradient(90deg, #ff6a00, #ee0979) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    padding: 12px 20px !important;
}
.gr-textbox textarea {
    font-size: 18px;
    font-weight: bold;
    color: #0072ff;
    text-align: center;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.HTML('<div id="title">💻 Laptop Price Predictor</div>')
    gr.Markdown("### ✨ Enter laptop specifications below to get a price prediction.")

    with gr.Row():
        with gr.Column(scale=2):
            with gr.Group():
                gr.Markdown("#### 🖥️ Laptop Specifications")
                brand = gr.Dropdown(choices=brand_options, label="Brand")
                name = gr.Dropdown(choices=name_options, label="Model Name")
                spec_rating = gr.Slider(minimum=0, maximum=100, step=0.1, label="Specification Rating")
                processor = gr.Dropdown(choices=processor_options, label="Processor")
                CPU = gr.Dropdown(choices=cpu_options, label="CPU")
                Ram = gr.Slider(minimum=2, maximum=64, step=1, label="RAM (in GB)")
                Ram_type = gr.Dropdown(choices=ram_type_options, label="RAM Type")
                ROM = gr.Slider(minimum=128, maximum=2048, step=128, label="ROM (in GB)")
                ROM_type = gr.Dropdown(choices=rom_type_options, label="ROM Type")
                GPU = gr.Dropdown(choices=gpu_options, label="GPU")
                display_size = gr.Slider(minimum=10, maximum=20, step=0.1, label="Display Size (in inches)")
                resolution_width = gr.Slider(minimum=1000, maximum=4000, step=10, label="Resolution Width")
                resolution_height = gr.Slider(minimum=700, maximum=3000, step=10, label="Resolution Height")
                OS = gr.Dropdown(choices=os_options, label="Operating System")
                warranty = gr.Slider(minimum=0, maximum=5, step=1, label="Warranty (in years)")

        with gr.Column(scale=1):
            gr.Markdown("#### 🔮 Prediction Result")
            output = gr.Textbox(label="Predicted Laptop Price", interactive=False)
            predict_button = gr.Button("🚀 Predict Price")

    predict_button.click(
        fn=predict_price,
        inputs=[brand, name, spec_rating, processor, CPU, Ram, Ram_type, ROM, ROM_type, GPU, display_size, resolution_width, resolution_height, OS, warranty],
        outputs=output
    )

    gr.Examples(
        examples=[
            ["HP", "Victus 15-fb0157AX Gaming Laptop", 73.0, "5th Gen AMD Ryzen 5 5600H", "Hexa Core, 12 Threads", 8, "DDR4", 512, "SSD", "4GB AMD Radeon RX 6500M", 15.6, 1920.0, 1080.0, "Windows 11 OS", 1],
            ["Acer", "Aspire 5 A515-58M NX.KHGSI.002 Gaming Laptop", 69.3, "13th Gen Intel Core i5 1335U", "10 Cores (2P + 8E), 12 Threads", 16, "LPDDR5", 512, "SSD", "Intel Integrated Iris Xe", 15.6, 1920.0, 1080.0, "Windows 11 OS", 1],
            ["Lenovo", "Yoga Slim 6 14IAP8 82WU0095IN Laptop", 66.0, "12th Gen Intel Core i5 1240P", "12 Cores (4P + 8E), 16 Threads", 16, "LPDDR5", 512, "SSD", "Intel Integrated Iris Xe", 14.0, 1920.0, 1200.0, "Windows 11 OS", 1]
        ],
        inputs=[brand, name, spec_rating, processor, CPU, Ram, Ram_type, ROM, ROM_type, GPU, display_size, resolution_width, resolution_height, OS, warranty],
        outputs=output,
        fn=predict_price,
        cache_examples=True,
    )

demo.launch()
