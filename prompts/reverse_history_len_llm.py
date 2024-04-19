import json


def add_markup(story, answers, current_turn, history_len):
    # Add markup for current turn and history_len previous turns in reverse order
    marked_story = story
    turn_count = len(answers)

    for i in range(current_turn, max(current_turn - history_len - 1, -1), -1):
        span_text = answers[i]["span_text"]
        turn_id = answers[i]["turn_id"]

        # Calculate the reverse index based on history_len
        reverse_index = current_turn - i

        # Add markup to story with reverse index
        marked_story = marked_story.replace(span_text, f"<{reverse_index}>{span_text}<{reverse_index}>")

    return marked_story


def transform_json(original_json, history_len):
    transformed_data = []

    for item in original_json['data']:
        no_answer_added = False  # Flag to track if "NO ANSWER" is added
        for i in range(len(item['questions'])):
            # Check if the current turn or any of the previous history_len turns have "unknown" answer
            unknown_answers = [item["answers"][j] for j in range(max(0, i - history_len), i + 1) if
                               item["answers"][j]["input_text"] == "unknown"]
            if unknown_answers:
                # Set span_text to "NO ANSWER" for the current turn
                for unknown_answer in unknown_answers:
                    unknown_answer["span_text"] = "NO ANSWER"

                # Add "NO ANSWER" at the end of the story for this turn
                item["story"] += " NO ANSWER"
                no_answer_added = True

            # 构建指令字符串
            instruction_lines = [item['story']]
            current_turn = i
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

            # Add markup to the transformed data
            story = instruction
            answers = item["answers"]

            # Add markup to story
            marked_story = add_markup(story, answers, current_turn, history_len)

            # Update story in data
            transformed_data[-1]["instruction"] = marked_story

        # If "NO ANSWER" is not added for this item, add it at the end of the story
        if not no_answer_added:
            item["story"] += " NO ANSWER"

    return transformed_data


def main():
    # 原始JSON文件的位置
    input_file = "dataset/tiqa-train-v3.json"
    # 新JSON文件的保存位置
    output_file = './finetune_data/v3/add_prompts/tiqa-train-v3-llm-h0-reverse.json'
    # 设置 history_len
    history_len = 0  # 假设设定为 2

    # 从文件读取原始JSON数据
    with open(input_file, 'r', encoding='utf-8') as file:
        original_json = json.load(file)

    # 转换JSON
    transformed_json = transform_json(original_json, history_len)

    # 将转换后的JSON数据保存到文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(transformed_json, file, ensure_ascii=False, indent=2)

    print("转换完成，数据已保存到：" + output_file)


if __name__ == "__main__":
    main()
