#!/usr/bin/env python3
import json
import re

def clean_text(text):
    if not isinstance(text, str):
        return text
    # Remove markdown bold markers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    return text.strip()

def clean_object(obj):
    if isinstance(obj, dict):
        return {k: clean_object(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_object(item) for item in obj]
    elif isinstance(obj, str):
        return clean_text(obj)
    return obj

def fix_json_file(input_file, output_file):
    try:
        # Read the entire file content
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Remove markdown code block markers
        content = re.sub(r'```json', '', content)
        
        # Remove any trailing % characters
        content = re.sub(r'%\s*$', '', content)
        
        # Split content into objects
        objects = []
        current_obj = ""
        brace_count = 0
        
        for char in content:
            if char == '{':
                brace_count += 1
                current_obj += char
            elif char == '}':
                brace_count -= 1
                current_obj += char
                if brace_count == 0 and current_obj.strip():
                    try:
                        obj = json.loads(current_obj)
                        # Clean all text in the object recursively
                        cleaned_obj = clean_object(obj)
                        objects.append(cleaned_obj)
                    except json.JSONDecodeError:
                        print(f"Warning: Skipping invalid JSON object: {current_obj[:100]}...")
                    current_obj = ""
            elif brace_count > 0:
                current_obj += char
        
        # Write the cleaned JSON to the output file
        with open(output_file, 'w') as f:
            json.dump(objects, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully fixed JSON file. Output written to {output_file}")
        print(f"Found {len(objects)} valid JSON objects")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    input_file = "sohn.json"
    output_file = "sohn_fixed.json"
    fix_json_file(input_file, output_file)
