from flask import Flask, request, render_template
import requests
import json
import openai
import os
import ast
import sys
import time

app = Flask(__name__)

OPENAI_KEY = "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"
openai.api_key = OPENAI_KEY

from pydantic import BaseModel

class Findings(BaseModel):
    Kidneys: str = None
    Ureters: str = None
    Urinary_bladder: str = None
    Reproductive_organs: str = None
    Lower_chest: str = None
    Liver: str = None
    Gallbladder: str = None
    Bile_ducts: str = None
    Spleen: str = None
    Pancreas: str = None
    Adrenal_glands: str = None
    Vasculature: str = None
    Lymph_nodes: str = None
    Bowel: str = None
    Peritoneum: str = None
    Abdominal_wall: str = None
    Bones: str = None

## Test transcript

"""
No stones. No renal mass. No hydronephrosis.

Small fat-containing omental hernia.

Mild atherosclerotic calcifications. No abdominal aortic aneurysm.
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript = request.form['transcript']
        summary = generate_summary_1(transcript)
        return render_template('index.html', summary=summary)
    return render_template('index.html')

def prettify_json(json_obj):
    prettified_string = '''<table style="
                            border-collapse: collapse;
                            width: 100%;
                            border: 0.1px solid #ddd;
                            ">
                            '''

    # Table headers with updated styles
    prettified_string += '''<tr style="
                            background-color: #f2f2f2;
                            ">
                            <th style="padding: 6px; text-align: left;">Key</th>
                            <th style="padding: 6px; text-align: left;">Value</th>
                            </tr>'''

    # Print each key-value pair in json_obj as a table row with new styles
    for key, value in json_obj.items():
        if value == "Unremarkable":
            value_style = "color: grey;"
        else:
            value_style = ""

        prettified_string += '''<tr>
                                <td style="padding: 6px; text-align: left; border-bottom: 1px solid #ddd;"><b>{}</b></td>
                                <td style="padding: 6px; text-align: left; border-bottom: 1px solid #ddd; {}">{}</td>
                                </tr>'''.format(key, value_style, value)

    # Close the table tag
    prettified_string += '</table>'
    
    return prettified_string




def get_template():
    findings_dict = {
        "Kidneys": None,
        "Ureters": None,
        "Urinary bladder": None,
        "Reproductive organs": None,
        "Lower chest": None,
        "Liver": None,
        "Gallbladder": None,
        "Bile ducts": None,
        "Spleen": None,
        "Pancreas": None,
        "Adrenal glands": None,
        "Vasculature": None,
        "Lymph nodes": None,
        "Bowel": None,
        "Peritoneum": None,
        "Abdominal wall": None,
        "Bones": None
    }
    print(findings_dict)
    return findings_dict

def generate_summary_1(text):
    template = get_template()

    prompt = "Transform the following transcript into the JSON object format given below. Populate the relevant parts of the transcript in the findings JSON. If there are no relevant part for a particular section, the finding is 'Unremarkable'. Only output the JSON, do not write anything else.\n\n" + \
            f"JSON format: {str(template)}\n\n" + \
            f"Transcript: {text}\n\n"

    print("\n\nPROMPT: ", prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {
        "role": "user",
        "content": prompt,
        }
        ],
        stream=True,
        max_tokens=600,
        temperature=0.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        )
    
    # Streaming version
    answer = ""
    for chunk in response:
        try:
            delta = chunk.choices[0].delta.content
            answer += delta
            for char in delta:
                print(char, end='')
                time.sleep(0.01)
                sys.stdout.flush()

        except:
            pass
    
    print("ANSWER: ", answer)

    # Non-streaming version
    # answer = response.choices[0].message.content
    # print("\n\nRESPONSE: ", answer)
    
    # Use ast.literal_eval to convert string to dictionary
    try:
        response_dict = ast.literal_eval(answer)
        print("\n\nAST casting passed 🟢✅")

        # Validate response with Pydantic model
        try:
            findings = Findings(**response_dict)
            print("\n\nSchema validation passed 🟢✅\n\n")

            prettified_string = prettify_json(response_dict)
            
            return prettified_string
        
        except Exception as e:
            print("error: ", e)
    except:
        print("ast literal eval failed")


    return prettified_string
    
    

if __name__ == '__main__':
    app.run(debug=True)
