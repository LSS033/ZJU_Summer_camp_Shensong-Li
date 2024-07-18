from flask import Flask, request, jsonify
from flask_cors import CORS
def get_prompt1(A,B,sentence):
    s1='Someone spoke '
    s1+=sentence
    s2='in the persona of '
    s2+=A
    s3='Please retell the sentence in the persona of'
    s3+=B
    s=s1+s2+s3
    return s

import requests
import json
API_KEY = "3Lb4fi8FzItECvmsnDrZURIb"
SECRET_KEY = "hO8MQLULNG6omSV2CbyIOO9MSRxkCVU1"
 
 
def main12(A,B,sentence):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while(1):
        s=sentence
        s=s+get_prompt1(A,B,sentence)
        payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": s
            }
        ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
 
        res = requests.request("POST", url, headers=headers, data=payload).json()
        return res['result']
 
 
 
 
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def get_model_en(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda:1",
                                                 quantization_config=bnb_config, trust_remote_code=True).eval()
    return model, tokenizer
'''
def get_model_zh(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda:0",quantization_config=bnb_config, trust_remote_code=True).eval()
    model.generation_config = GenerationConfig.from_pretrained(model_path, trust_remote_code=True)
    return model, tokenizer
'''
def get_model_zh(model_path):
    model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return model, tokenizer



app = Flask(__name__)
CORS(app) 




@app.route('/chat', methods=['POST'])
def handle_chat():
    torch.cuda.empty_cache()
    #gc.collect()
    if request.method == 'POST':
        # 获取前端发送的 JSON 数据
        print('aaaaaaa')
        data = request.json
        # 解析 JSON 数据中的各个字段
        input_text = data['input_text']
        language = find_language(input_text)
        print(language)
        # language = data['language']
        # original_personality = DDGCN_predic_single_post2(post=input_text)
        original_personality = data['original_personality']
        target_personality = data['target_personality']
        original_personality=original_personality[:4]
        target_personality=target_personality[:4]
        print(data)
        # 确保所有必要的字段都存在
        if all([input_text,  original_personality, target_personality, language_model]):         
            
            output=main12(original_personality,target_personality,input_text)
            # 返回响应给前端
            
            return jsonify({
                'output':output,#混淆结果文本
                'original_personality':original_personality,
                'target_personality':target_personality
            })
    
        else:
        #     # 如果缺少必要字段，返回错误信息
            return jsonify({'error': 'Missing required fields in the request'})
    else:
        # 如果请求方法不是 POST，返回错误信息
        return jsonify({'error': 'Invalid request method. Only POST is allowed.'})

if __name__ == '__main__': # 使用指定的 IP 地址和端口号启动 Flask 应用 
    
    app.run(host='0.0.0.0', port=5000, debug=False)
