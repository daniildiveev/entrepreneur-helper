from simpletransformers.question_answering import QuestionAnsweringModel
from simpletransformers.question_answering import QuestionAnsweringArgs

model_args = QuestionAnsweringArgs()
model_args.n_best_size = 1
model_args.use_cuda = False
model = QuestionAnsweringModel(
    "roberta",
    "deepset/roberta-base-squad2",
    args=model_args
)