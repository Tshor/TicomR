import requests
import json
import os
import json
import requests

def call_api(instruction_content, max_retries=2):
    url = "http://10.119.130.187:8024/v1/chat/completions"
    for attempt in range(max_retries):
        try:
            payload = {
                "model": "string",
                "messages": [
                    {"role": "user", "content": instruction_content}
                ],
                "do_sample": True,
                "temperature": 0.05,
                "top_p": 0.2,
                "n": 1,
                "max_tokens": 512,
                "stream": False
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"API调用失败，重试 {attempt + 1}/{max_retries}，状态码: {response.status_code}, 响应: {response.text}")
        except requests.RequestException as e:
            print(f"请求异常，重试 {attempt + 1}/{max_retries}，异常信息: {e}")

    return "Error"

def process_files(input_json_file, output_json_file):
    with open(input_json_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        results = []

        for item in data:
            instruction = item.get('instruction', '').strip()
            if instruction:
                predicted_label = call_api(instruction)
                result = {
                    "instruction": instruction,
                    "predicted_label": predicted_label
                }
                results.append(result)
                print(f"处理完成: 预测标签: {predicted_label}")

    with open(output_json_file, 'w', encoding='utf-8') as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)


# 调用这个函数来开始处理
process_files('./finetune_data/v3/no_prompts/tiqa-dev-v3-llm-ha.json', './finetune_data/v3/predict/tiqa-dev-v3-llm-ha-predict.json')


