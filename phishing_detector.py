import tkinter as tk
from tkinter import messagebox
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

# Define the model path to the extracted folder
model_path = "C:/Users/owner/OneDrive/Desktop/phishing_detector_model"  # Update to your model's location
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Set device to GPU if available
device = 0 if torch.cuda.is_available() else -1

# Create a pipeline for text classification
phishing_detector = pipeline("text-classification", model=model, tokenizer=tokenizer, device=device)

# Function to classify the email text entered in the GUI
def classify_email():
    email_text = email_entry.get("1.0", tk.END).strip()  # Get text from the Tkinter Text widget
    if not email_text:
        messagebox.showwarning("Input Error", "Please enter email text to classify.")
        return

    # Run the text through the model
    result = phishing_detector(email_text)
    label = result[0]["label"]
    score = result[0]["score"]

    # Interpret results
    classification = "Phishing" if label == "LABEL_1" else "Legitimate"
    confidence = round(score * 100, 2)

    # Display the result in the GUI
    result_label.config(text=f"Classification: {classification} (Confidence: {confidence}%)")

# Set up the GUI window
root = tk.Tk()
root.title("Phishing Email Detector")
root.geometry("500x300")

# Add instructions label
instructions = tk.Label(root, text="Enter the email text below to classify it as phishing or legitimate.")
instructions.pack(pady=10)

# Add a text entry box for the email content
email_entry = tk.Text(root, height=10, width=50)
email_entry.pack(pady=5)

# Add a classify button
classify_button = tk.Button(root, text="Classify Email", command=classify_email)
classify_button.pack(pady=10)

# Add a label to display the classification result
result_label = tk.Label(root, text="Classification: ", font=("Arial", 14))
result_label.pack(pady=10)

# Run the main loop
root.mainloop()
