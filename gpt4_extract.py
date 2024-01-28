from openai import OpenAI
import json
import tqdm
import random
import os

client = OpenAI()

if __name__ == "__main__":
    data = []
    with open('outputs.jsonl', 'r') as f:
        for line in f:
            data.append(json.loads(line))
    random.shuffle(data)
    print(len(data))

    # Decide whether to start from scratch
    count = 0
    if os.path.exists('output_extracted.jsonl'):
        with open('output_extracted.jsonl') as f:
            for line in f:
                count += 1
        f = open('output_extracted.jsonl', 'a')
        print(f'output_extracted.jsonl already exists with {count} lines')
    else:
        f = open('output_extracted.jsonl', 'w')

    for i, entry in tqdm.tqdm(enumerate(data)):
        if i < count:
            continue

        # Formulate the user request;
        system_prompt = """
You are a helpful assistant to help me analyze a given exam question and solution. There are three things you need to do:
image_question: decide whether the question requires reading a figure to answer.
image_answer: decide whether the answer to the question should be a figure instead of text.
short_answer: decide the question can be answered with a short phrase instead of a long sentence.
answer: extract a short phrase from the solution as the answer.

Return your answer in JSON format like:
{
    "image_question": True/False,
    "image_answer": True/False,
    "short_answer": True/False,
    "answer": 'a short phrase',
}
"""
        user_request = f"""
Question: {entry["question"]}
Solution: {entry["solution"]}
"""
        # Formulate the response;
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_request}],
            temperature=0.0,
        )
        output = response.choices[0].message.content
        output = output.replace('true', 'True')
        output = output.replace('false', 'False')

        try:
            answer = eval(output)
            answer['question'] = entry['question']
            print(answer)

            entry.update(answer)

            f.write(json.dumps(entry) + '\n')
        except Exception:
            continue

    f.close()