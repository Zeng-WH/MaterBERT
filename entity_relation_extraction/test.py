from spert import input_reader
from transformers import BertTokenizer


input_reader_cls = input_reader.JsonInputReader

type_path = '/home1/wlw2020/head_motion/SpERT/spert-master/data/conll04/conll04_types.json'
train_path = '/home1/wlw2020/head_motion/SpERT/spert-master/scripts/data/datasets/conll04/conll04_train.json'
vaild_path = '/home1/wlw2020/head_motion/SpERT/spert-master/scripts/data/datasets/conll04/conll04_dev.json'
tokenizer = BertTokenizer.from_pretrained(
    'bert-base-cased',
    do_lower_case=False,
)

reader_input = input_reader_cls(
    '/home1/wlw2020/head_motion/SpERT/spert-master/scripts/data/datasets/conll04/conll04_types.json',
    tokenizer,
    100,
    10,
    logger=None
)
train_label, valid_label = 'train', 'valid'
reader_input.read({train_label:train_path, valid_label: vaild_path})
train_dataset = reader_input.get_dataset(train_label)
print('bupt')