import datasets
import re
import lm_eval.tasks.newyorker_caption_contest.process_query as process_query
import lm_eval.tasks.newyorker_caption_contest.matching_prompts as matching_propts

shot_record_path = "lm_eval\\tasks\\newyorker_caption_contest\shot_record.txt"


def preprocess(text):
    text = text.strip()
    # NOTE: Brackets are artifacts of the WikiHow dataset portion of HellaSwag.
    text = text.replace(" [title]", ". ")
    text = re.sub("\\[.*?\\]", "", text)
    # text = text.replace("  ", " ")
    return text


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        # ctx = doc["ctx_a"] + " " + doc["ctx_b"].capitalize()
        out_doc = {
            "query": process_query.format_chatgpt_input(doc),
            "choices": [preprocess(caption) for caption in doc["caption_choices"]],
            "gold": doc["label"],
        }
        return out_doc

    # with open(shot_record_path, 'w') as f:
    #     f.write(str(0))

    return dataset.map(_process_doc)


# def doc_to_text_processor(doc):
#     # print(doc.keys())
#     query = process_query.format_chatgpt_input(doc)
#     choices = [preprocess(caption) for caption in doc["caption_choices"]]

#     with open(shot_record_path, 'r') as f:
#         shot = int(f.read())

#     header = ""
#     promt = f"{query}\nChoices:\nA: {choices[0]}\nB: {choices[1]}\nC: {choices[2]}\nD: {choices[3]}\nE: {choices[4]}\n\nWhich of the 5 options (A, B, C, D, or E) is the caption that truly corresponds to the cartoon?\n~~~"

#     if shot == 0:
#         header += matching_propts._PROMPT_SYSTEM_MATCHING_V1
#         header += "\n~~~\nrole: user\n" + matching_propts._PROMPT_USER_MATCHING_DIRECT_ANSWER_V1 + "\n"
#         promt = header + promt

#     if shot < 5:
#         with open(shot_record_path, 'w') as f:
#             f.write(str(shot + 1))
#     else:
#         with open(shot_record_path, 'w') as f:
#             f.write(str(0))
#             print('clear')

#     return promt
