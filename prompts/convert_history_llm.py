import json

# def transform_json(original_json):
def transform_json(original_json, history_len):
    transformed_data = []

    for item in original_json['data']:
        # history_len = len(item['questions'])  # 获取当前item中的history_len

        for i in range(len(item['questions'])):
            # 构建指令字符串
            instruction_lines = [item['story']]
            for j in range(max(0, i - history_len), i + 1):
                long_question = item['questions'][j]['input_text']
                if j < i:
                    # 添加历史问题以及对应答案
                    long_question += f' {item["answers"][j]["turn_id"]}. {item["answers"][j]["input_text"]}'
                instruction_lines.append(f"{item['questions'][j]['turn_id']}.{long_question}")

            instruction = "\n".join(instruction_lines)

            # 构建输出字符串
            output = f"{item['answers'][i]['turn_id']}.{item['answers'][i]['input_text']}"

            transformed_data.append({
                "instruction": instruction,
                "input": "",
                "output": output
            })

    return transformed_data


def main():
    # 原始JSON文件的位置
    input_file = "dataset/tiqa-train-v3.json"
    # 新JSON文件的保存位置
    output_file = 'finetune_data/v3/no_prompts/tiqa-train-v3-llm-h4.json'
    # 设置 history_len
    history_len = 4  # 假设设定为 3

    # 从文件读取原始JSON数据
    with open(input_file, 'r', encoding='utf-8') as file:
        original_json = json.load(file)

    # 转换JSON
    transformed_json = transform_json(original_json, history_len)
    # transformed_json = transform_json(original_json)

    # 将转换后的JSON数据保存到文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(transformed_json, file, ensure_ascii=False, indent=2)

    print("转换完成，数据已保存到：" + output_file)

if __name__ == "__main__":
    main()
