from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import datetime  # <--- NEW: Library to check the clock

app = Flask(__name__)

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print(f"Loading {model_id}...")
try:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_input = user_data.get('question')

    if not user_input:
        return jsonify({"error": "Please say something"}), 400

    # 1. GET CURRENT TIME
    # We get the time from YOUR computer
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. INJECT TIME INTO THE PROMPT
    # We add a <|system|> tag to give the bot context before the user speaks.
    # We tell it: "You are a helpful bot. The current time is [NOW]."
    prompt = (
        f"<|system|>\n"
        f"You are a helpful assistant. The current time is {now}.\n"
        f"</s>\n"
        f"<|user|>\n{user_input}</s>\n"
        f"<|assistant|>\n"
    )

    # 3. Tokenize
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    # 4. Generate
    outputs = model.generate(
        input_ids,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

    # 5. Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract Answer
    answer = generated_text.split("<|assistant|>\n")[-1].strip()

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    print("Time-Aware Bot is ready!")
    app.run(debug=True, port=5000)