from flask import Flask, request, jsonify
import torch
from torch import nn
from flask_cors import CORS
from transformers import RobertaTokenizer
from transformers import T5ForConditionalGeneration
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')


app = Flask(__name__)
CORS(app)

state_dict_code2pc = torch.load(
    'models/code2pc.pt', map_location=torch.device('cpu'))
state_dict_tx2Code = torch.load(
    'models/tx2Code.pt', map_location=torch.device('cpu'))

device = torch.device('cpu')

code2pcModel = T5ForConditionalGeneration.from_pretrained(
    'Salesforce/codet5-base')
code2pcModel.load_state_dict(state_dict_code2pc)
tx2CodeModel = T5ForConditionalGeneration.from_pretrained(
    'Salesforce/codet5-base')
tx2CodeModel.load_state_dict(state_dict_tx2Code)

code2pcModel.to(device)
tx2CodeModel.to(device)


def getPseudocode(code):

    #variable to store final result
    result = []
    prefix = "Generate Pseudocode: "

    #split the code at new line
    input_code_list = code.split('\n')
    print(input_code_list)

    for i in range(0, len(input_code_list)):
        text = prefix + input_code_list[i]
        input_ids = tokenizer(text, return_tensors="pt").input_ids
        input_ids = input_ids.to(device)
        generated_ids = code2pcModel.generate(
        input_ids, max_length=128, top_p=0.95, top_k=50)
        ps = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        result.append((str(i+1) + '. '+ str(ps)))
    return '\n'.join(result)


def getCode(text):
    print('TEXT RECIEVED - ' + text)
    prefix = "Generate Python: "
    text = prefix + text
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    input_ids = input_ids.to(device)
    # print('INPUT IDS - ' + input_ids)
    generated_ids = tx2CodeModel.generate(
        input_ids, max_length=128, top_p=0.95, top_k=50)
    result = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    print(result)
    return(result)


@app.route('/', methods=['GET'])
def helloWorld():
    return jsonify({'data': 'hello world from server'})


@app.route('/generatePseudocode', methods=['POST'])
def generatePseudocode():
    code = request.json['code']
    print(code)

    pseudocode = getPseudocode(code)

    return jsonify({'pseudocode': pseudocode})


@app.route('/generateCode', methods=['POST'])
def generateCode():
    text = request.json['text']
    print(text)

    code = getCode(text)

    return jsonify({'code': code})


if __name__ == '__main__':
    app.run()
