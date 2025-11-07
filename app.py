"""
CroweLogic-Pharma Gradio Interface for Hugging Face Spaces
Pharmaceutical AI Assistant powered by Ollama
"""

import gradio as gr
import requests
import json
import os

# Ollama API endpoint
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = "CroweLogic-Pharma:latest"

def query_model(prompt, temperature=0.7, max_tokens=2000):
    """Query the CroweLogic-Pharma model"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response generated")
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error connecting to model: {str(e)}"


def create_demo():
    """Create the Gradio interface"""

    # Example prompts
    examples = [
        ["What are the neuroprotective mechanisms of hericenones from Lion's Mane mushroom?"],
        ["Explain the anticancer properties of ganoderic acids from Reishi mushroom."],
        ["Design a Phase II clinical trial for testing Lion's Mane extract in Alzheimer's patients."],
        ["What are the key bioactive compounds in Turkey Tail mushroom and their immunomodulatory effects?"],
        ["Analyze the ADME-Tox properties of beta-glucans from medicinal mushrooms."],
        ["What are the therapeutic applications of cordycepin from Cordyceps mushrooms?"],
    ]

    # Custom CSS
    custom_css = """
    .gradio-container {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .gr-button-primary {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        border: none;
    }
    """

    with gr.Blocks(css=custom_css, title="CroweLogic-Pharma AI") as demo:
        gr.Markdown("""
        # 🍄 CroweLogic-Pharma: AI-Powered Pharmaceutical Research

        An advanced AI assistant specializing in:
        - **Pharmaceutical Research** & Drug Discovery
        - **Mycopharmacology** (Mushroom-Derived Therapeutics)
        - **Medicinal Chemistry** & ADME-Tox Prediction
        - **Clinical Trial Design** & Regulatory Compliance
        - **Natural Product Drug Discovery**

        ---
        """)

        with gr.Row():
            with gr.Column(scale=2):
                prompt_input = gr.Textbox(
                    label="Ask CroweLogic-Pharma",
                    placeholder="Ask about pharmaceutical research, drug discovery, medicinal mushrooms, clinical trials, or regulatory compliance...",
                    lines=4
                )

                with gr.Row():
                    temperature_slider = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature (Creativity)",
                        info="Lower = More focused, Higher = More creative"
                    )

                    max_tokens_slider = gr.Slider(
                        minimum=500,
                        maximum=4000,
                        value=2000,
                        step=500,
                        label="Max Response Length",
                        info="Maximum tokens in response"
                    )

                submit_btn = gr.Button("🔬 Analyze", variant="primary", size="lg")

            with gr.Column(scale=2):
                output = gr.Textbox(
                    label="Response",
                    lines=20,
                    show_copy_button=True
                )

        gr.Examples(
            examples=examples,
            inputs=prompt_input,
            label="Example Queries"
        )

        gr.Markdown("""
        ---

        ## 📚 Knowledge Domains

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">

        <div>
        <h3>🍄 Mycopharmacology</h3>
        <ul>
        <li>Hericenones & Erinacines (Lion's Mane)</li>
        <li>Ganoderic Acids (Reishi)</li>
        <li>PSK/PSP (Turkey Tail)</li>
        <li>Cordycepin (Cordyceps)</li>
        <li>Beta-Glucans (Various)</li>
        </ul>
        </div>

        <div>
        <h3>💊 Pharmaceutical Research</h3>
        <ul>
        <li>Drug Design & SAR Analysis</li>
        <li>ADME-Tox Prediction</li>
        <li>Target Identification</li>
        <li>Molecular Docking</li>
        <li>QSAR Modeling</li>
        </ul>
        </div>

        <div>
        <h3>🧪 Clinical Applications</h3>
        <ul>
        <li>Neurodegenerative Diseases</li>
        <li>Cancer Immunotherapy</li>
        <li>Cognitive Enhancement</li>
        <li>Anti-inflammatory Therapies</li>
        <li>Metabolic Disorders</li>
        </ul>
        </div>

        <div>
        <h3>📋 Regulatory & Trials</h3>
        <ul>
        <li>Clinical Trial Design</li>
        <li>FDA/EMA Compliance</li>
        <li>IND Applications</li>
        <li>Safety Assessment</li>
        <li>Efficacy Endpoints</li>
        </ul>
        </div>

        </div>

        ---

        ## ℹ️ About

        **CroweLogic-Pharma** is built on a fine-tuned language model with specialized training in:
        - 300+ curated pharmaceutical examples
        - ChEMBL drug target database integration
        - Published research on medicinal mushrooms
        - Clinical trial methodologies
        - Regulatory compliance frameworks

        **Version**: 2.0.0 | **Training Data**: Pharmaceutical literature, ChEMBL, expert mycology knowledge

        ---

        ## ⚠️ Disclaimer

        This AI assistant is for **research and educational purposes only**. Always consult with qualified healthcare professionals and conduct proper validation studies. No information provided should be considered medical advice or used for self-treatment.

        ---

        **Built with 🍄 for advancing mushroom-derived therapeutics**

        📧 Contact: [GitHub](https://github.com/MichaelCrowe11/crowelogic-pharma-model)
        """)

        # Connect the button
        submit_btn.click(
            fn=query_model,
            inputs=[prompt_input, temperature_slider, max_tokens_slider],
            outputs=output
        )

        # Also submit on Enter key
        prompt_input.submit(
            fn=query_model,
            inputs=[prompt_input, temperature_slider, max_tokens_slider],
            outputs=output
        )

    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
