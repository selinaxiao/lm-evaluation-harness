from datasets import load_dataset, DatasetDict
from huggingface_hub import notebook_login

file_path = "matching_1.csv"
train_set = load_dataset('csv', data_files={'train': "matching_train.csv"})
validation_set = load_dataset('csv', data_files={'train': "matching_validation.csv"})
test_set = load_dataset('csv', data_files={'train': "matching_test.csv"})
# dataset2 = load_dataset(
#     'csv', 
#     data_files="matching_train_empty.csv", 
#     delimiter=',',  # Change this according to your file's delimiter
#     encoding='utf-8'  # Specify the encoding if necessary
# )

def transform_column(example):
    # Splitting the 'text' column string into a list of words
    # 'text' is the column you want to transform
    example['entities'] = example['entities'].split(',,')
    example['caption_choices'] = example['caption_choices'].split(',,')
    example['questions'] = [example['questions']]
    return example

# Apply the transformation function to the dataset
# The transformation is applied only to the 'text' column, as defined in your function
# transformed_dataset = dataset.map(transform_column, batched=False)
# print(dataset.column_names)
# print(dataset['train']['contest_number'])
# transformed_dataset2 = dataset2.map(transform_column, batched=False)

dataset_dict = DatasetDict({
    'train': train_set.map(transform_column, batched=False)['train'], 
    'validation': validation_set.map(transform_column, batched=False)['train'], 
    'test': test_set.map(transform_column, batched=False)['train']  # Rename the split to 'test'
})

# dataset_dict2 = DatasetDict({
#     'train': transformed_dataset['train']  # Rename the split to 'test'
# })



# Optionally, save your dataset locally for inspection before uploading
# Replace 'your_dataset_name' with a unique name for your dataset
dataset_dict.save_to_disk('matching')
# dataset_dict2.save_to_disk('matching')

# Now, push your dataset to the Hugging Face Hub
# Replace 'your_dataset_name' with the name you want for your dataset on the hub
# Replace 'your_username' with your Hugging Face username
dataset_dict.push_to_hub('selinax10010/matching')

# This will upload the dataset to your Hugging Face account under the specified name



