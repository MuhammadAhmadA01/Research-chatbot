import openai
from openai import OpenAI
from sklearn.model_selection import train_test_split
import json
import time

client = openai.OpenAI(api_key=api_key)

def label_data(data):
    
    prompt = f"""
    you will write a neutral text for the provided text. 
    Text: "
       {data}
       "
Note: Neutral text means how you will write about the same topic, discussed in paragraph. Write the text in your style which will cover all the things and I'm calling your written Text "Neutral Text ". So your task is to write a neutral text other things are for your assistant. Write like its your own text not mention words like "the paragraph discusses." you will write like you are writing for first time   
Response: response will only contain neutral text no explanation nothing else. 
    """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": prompt}
    ]
    )
    
    response = completion.choices[0].message.content  
    return response

def append_to_json_and_file(data, label, json_file_path, data_file_path):
    try:
        # Load existing data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        data_list = []

    # Append the new data and label to the list
    data_list.append({ "prompt": label, "ans": data})

    # Write the updated list back to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)

    # Append the new data and label to the data file
    with open(data_file_path, 'a', encoding='utf-8') as file:
        file.write(f"{data}\n{label}\n\n")

def process_file(file_path, json_file_path, data_file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        paragraphs = content.split("\n\n")
        start_time = time.time()
        for i, s in enumerate(paragraphs):
            iteration_start_time = time.time()
            if i > 0 and i<=500:
                print(i)
                label = label_data(s)
                append_to_json_and_file(s, label, json_file_path, data_file_path)
                # Calculate the delay needed to achieve approximately 3 iterations per minute      
                delay_seconds = 60 / 3 - (time.time() - start_time) % (60 / 3)
                if delay_seconds > 0:
                    time.sleep(delay_seconds)
            iteration_end_time = time.time()    
            processing_time = iteration_end_time - iteration_start_time
            print(f"Processing time for iteration {i}: {processing_time:.2f} seconds")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_files(file_paths, json_file_path, data_file_path):
    for file_path in file_paths:
        process_file(file_path, json_file_path, data_file_path)

# Example usage
file_paths =   ["cleaned.txt"]
json_file_path = "Assignment_5.json"
data_file_path = "cleaned.txt"

process_files(file_paths, json_file_path, data_file_path)