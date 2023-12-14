import requests
import json
import openai
import os
import ast
import sys
import time
from dotenv import load_dotenv
from pydantic import BaseModel
from flask import Flask, request, render_template

load_dotenv('openai.env')

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

generate_impression = True # Set to True to generate impression (TD: accept as argparse argument)
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

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    summary = ""
    if request.method == 'POST':
        transcript = request.form['transcript']
        # yield render_template('index.html', transcript=transcript, summary=summary)
        
        summary, impression = generate_summary_1(transcript, generate_impression=generate_impression)
        
        if generate_impression:
            return render_template('index.html', summary=summary, transcript=transcript, impression=impression)
        else:
            return render_template('index.html', summary=summary, transcript=transcript)
    
    return render_template('index.html')

def prettify_json(json_obj):
    # this fn needs cleanup BIG TIME
    prettified_string = ""
    prettified_html = '''<table style="
                            border-collapse: collapse;
                            width: 100%;
                            border: 0.1px solid #ddd;
                            ">
                            '''

    prettified_html += '''<tr style="
                            background-color: #f2f2f2;
                            ">
                            <th style="padding: 6px; text-align: left;">Key</th>
                            <th style="padding: 6px; text-align: left;">Value</th>
                            </tr>'''

    for key, value in json_obj.items():
        if value == "Unremarkable":
            value_style = "color: grey;"
        else:
            value_style = ""

        prettified_html += '''<tr>
                                <td style="padding: 6px; text-align: left; border-bottom: 1px solid #ddd;"><b>{}</b></td>
                                <td style="padding: 6px; text-align: left; border-bottom: 1px solid #ddd; {}">{}</td>
                                </tr>'''.format(key, value_style, value)
        prettified_string += f"{key}: {value} \n"

    prettified_html += '</table>'
    
    return prettified_html, prettified_string


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
    
    return findings_dict

def generate_impression_1(findings):
    prompt = "Generate an impression based for the findings in a style similar to the given examples. Only output the impression, do not write anything else.\n\n" + \
            "EXAMPLES::\n\n\n" + \
            "Findings:\n" + \
            "Lower chest: Unremarkable \nLiver: Unremarkable. \nGallbladder: Unremarkable. \nBile ducts: Unremarkable. \nSpleen: Unremarkable. \nPancreas: Unremarkable. \nAdrenal glands: Unremarkable. \nKidneys and Ureters: Unremarkable. \nLymph Nodes: Mild bilateral inguinal lymphadenopathy, likely reactive. \nVasculature: Unremarkable. \nBowel: Unremarkable. \nReproductive organs: Unremarkable. \nBladder: Unremarkable. \nPeritoneum: Unremarkable. \nAbdominal wall: There is an ill-defined phlegmon in the right anterior abdominal wall measuring approximately 2.4 x 1.5 x 1.7 cm (series 900 image 76). There is marked interstitial edema and fat stranding along the right anterior abdominal wall, and mildly edematous appearance of the right rectus abdominis. \nBones: Unremarkable\n\n" + \
            "Impression: \n" + \
            "There is an ill-defined phlegmon in the right anterior abdominal wall measuring approximately 2.4 x 1.5 x 1.7 cm with marked associated interstitial edema and fat stranding along the right anterior abdominal wall. Findings concerning for severe cellulitis with phlegmon.  No additional acute abnormality in the abdomen or pelvis. \n\n\n" + \
            "Findings:\n" + \
            "ABDOMEN AND PELVIS Liver: Mild hepatic steatosis. \nPortal veins: Unremarkable. \nGallbladder and bile ducts: Unremarkable. \nSpleen: Unremarkable. \nPancreas: Unremarkable. \nKidneys: Large exophytic cyst off the superior pole of the kidney without suspicious features. Additional simple appearing cysts bilaterally. \nAdrenal glands: Unremarkable. \nAorta and IVC: Unremarkable. \nStomach, duodenum and small bowel: Unremarkable. \nColon: Unremarkable. \nFree intraperitoneal air or fluid: None. \nMesentery, omentum and retroperitoneum: Unremarkable. \nLymph Nodes: No suspicious lymph nodes. \nBladder: Unremarkable. \nPelvis organs: Unremarkable. \nAbdominal wall: Unremarkable. \nOther Soft tissues: Unremarkable. \nOther: None. \nBones: No fractures identified.\n\n" + \
            "Impression: \n" + \
            "No traumatic injury to the chest, abdomen or pelvis.  Congenital aortic arch variant without evidence of traumatic abnormality. \n\n\n" + \
            f"Findings: {str(findings)}\n\n" + \
            "Impression: \n"
    
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
        frequency_penalty=0.0
        )
    
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

    # print("\n\nIMPRESSION: ", answer)
    return answer

def generate_summary_1(text, generate_impression=False):
    template = get_template()

    prompt = "Transform the following transcript into the JSON object format given below. Populate the relevant parts of the transcript in the findings JSON. If there are no relevant part for a particular section, the finding is 'Unremarkable'. Only output the JSON, do not write anything else.\n\n" + \
            f"JSON format: {str(template)}\n\n" + \
            f"Transcript: {text}\n\n"

    print("\n\nInstantiating prompt... ⏳\n\n")

    start = time.time()

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
    
    end = time.time()

    print("Time taken to generate FINDINGS (seconds): ", end - start)
    
    # Non-streaming version
    # answer = response.choices[0].message.content
    # print("\n\nRESPONSE: ", answer)
    # remove first 7 and last three characters for turbo mode
    # answer = answer[7:-3]
    
    try:
        response_dict = ast.literal_eval(answer)
        print("\n\nAST casting passed 🟢✅")
        time.sleep(1)
        
        # Validate against Pydantic schema declaration
        try:
            findings = Findings(**response_dict)
            print("\n\nSchema validation passed 🟢✅\n\n")

            prettified_html, prettified_findings_string = prettify_json(response_dict)
            
            if generate_impression:
                print("STREAM MODE: ON")
                print("\n\nGenerating impression ⏳...\n\n")
                
                try:
                    impression = generate_impression_1(prettified_findings_string)
                    print("\n\nImpression generated successfully 🟢✅\n\n")
                    time.sleep(1)

                except:
                    print("Impression generation failed")
                    impression = "Impression generation failed"

                return prettified_html, impression

            return prettified_html
        
        except Exception as e:
            print("error: ", e)
    except:
        print("ast literal eval failed")

    return prettified_html
    
    

if __name__ == '__main__':
    app.run(debug=True)
