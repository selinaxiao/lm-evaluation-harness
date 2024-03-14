import lm_eval.tasks.newyorker_caption_contest.matching_prompts as matching_prompts

_FD_MODE = 4


def format_chatgpt_input(d):
    '''
    mode=1 is location
    mode=2 is location/description
    mode=3 is location/description/uncanny
    mode=4 is location/description/uncanny/entities (from paper)
    '''

    global _FD_MODE
    mode = _FD_MODE

    # lets fix entities...
    fixed_entities = []
    for ent in d['entities']:
        ent = ent.split('#')[0]
        ent = ent.replace('&redirect=no', '')
        ent = ent.replace('https://en.wikipedia.org/?title=', '/wiki/')
        ent = ent.split('/wiki/')[1]
        ent = ent.replace('%27s', "'")
        ent = ent.replace('(disambiguation)', '')
        ent = ent.replace('_', ' ')
        ent = ' '.join(ent.split())
        fixed_entities.append(ent)

    if mode == 4:
        return 'scene location: {}\ndescription: {}\nuncanny description: {}\nentities: {}'.format(
            d['image_location'],
            d['image_description'],
            d['image_uncanny_description'],
            ', '.join(fixed_entities))
    if mode == 3:
        return 'scene location: {}\ndescription: {}\nuncanny description: {}'.format(
            d['image_location'],
            d['image_description'],
            d['image_uncanny_description'])
    if mode == 2:
        return 'scene location: {}\ndescription: {}'.format(
            d['image_location'],
            d['image_description'])
    if mode == 1:
        return 'scene location: {}'.format(
            d['image_location'])

    if mode == 0:
        return 'a new yorker cartoon'


def generate_request_matching_few_shot(query, few_shots):
    global _PROMPT_SYSTEM_MATCHING_DIRECT_ANSWER_V1, _PROMPT_USER_MATCHING_DIRECT_ANSWER_V1, _RESPONSE_ASSISTANT_MATCHING_DIRECT_ANSWER_V1

    messages = [{"role": "system", "content": _PROMPT_SYSTEM_MATCHING_DIRECT_ANSWER_V1}]

    for idx, fs in enumerate(few_shots):

        extra = 'Thanks! How about this one?\n' if idx != 0 else (_PROMPT_USER_MATCHING_DIRECT_ANSWER_V1 + '\n')
        messages.append({
            'role': 'user',
            'content': extra + '\n{}\nChoices:\n{}\n\nWhich of the 5 options (A, B, C, D, or E) is the caption that truly corresponds to the cartoon?'.format(
                format_chatgpt_input(fs),
                '\n'.join(['{}: {}'.format(cidx, c) for cidx, c in zip('ABCDE', fs['caption_choices'])]))})
        messages.append({
            'role': 'assistant',
            'content': 'Answer: {}'.format(fs['label'])})

    extra = 'Thanks! How about this one?\n'
    messages.append({
        'role': 'user',
        'content': extra + '\n{}\nChoices:\n{}\n\nWhich of the 5 options (A, B, C, D, or E) is the caption that truly corresponds to the cartoon?'.format(
            format_chatgpt_input(query),
            '\n'.join(['{}: {}'.format(cidx, c) for cidx, c in zip('ABCDE', query['caption_choices'])]))})

    return messages


def generate_request_matching(query, few_shots=None):
    if few_shots:
        return generate_request_matching_few_shot(query, few_shots)

    global _PROMPT_SYSTEM_MATCHING_V1, _PROMPT_USER_MATCHING_V1, _RESPONSE_ASSISTANT_MATCHING_V1

    messages = [{"role": "system", "content": _PROMPT_SYSTEM_MATCHING_V1}]

    messages.append({
        'role': 'user',
        'content': _PROMPT_USER_MATCHING_V1}
    )

    messages.append({
        'role': 'assistant',
        'content': _RESPONSE_ASSISTANT_MATCHING_V1}
    )

    messages.append({
        'role': 'user',
        'content': ('OK. Here is a description of the cartoon followed by the five choices.'
                    '\n\n{}\n\nChoices:\n{}\n\nWhich of the 5 options (A, B, C, D, or E) is the best fit? Think step-by-step and finish your response with "Answer: X" where X is either A, B, C, D, or E.'.format(
                        format_chatgpt_input(query),
                        '\n'.join(['{}: {}'.format(cidx, c) for cidx, c in zip('ABCDE', query['caption_choices'])])))})

    return messages
