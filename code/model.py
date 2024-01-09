import os
import openai
import json

openai.api_key = "sk-"  # os.getenv("OPENAI_API_KEY")


def ask_question(question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )

    return completion.choices[0].message


def get_context(file):
    file_path = "..\output_data\\" + file
    with open(file_path, "r", encoding="utf-8") as file:
        if "json" in file_path:
            data = json.load(file)
        else:
            data = file.read()
    return data


if __name__ == "__main__":
    context = get_context("sample_contract.txt")
    print("context: ", context)
    # question = "What is the least expensive item in this invoice?\nGive me the answer in this format:\nItem: Price"
    # question = "What is the address of the receiver?"
    question = "What type of contract is this? Who is this contract in between?"
    # question = "What is the NDA about?"
    # formatted_question = "This is data extracted from an invoice: \n\n" + json.dumps(context) + "\n\n" + question
    formatted_question = (
        "This is data extracted from a document: \n\n"
        + str(context)
        + "\n\n"
        + question
    )
    print("formatted_question: ", formatted_question)
    answer = ask_question(formatted_question)
    print()
    print()
    print(answer["content"])
