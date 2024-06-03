# TicomR
TiComR: A Prompt-based Tibetan Conversational Reading Comprehension Model

## 模型简介
现有的对话型阅读模型在中英文对话型阅读理解任务中表现出色，但由于藏文在语法结构、表达方式等方面同中英文有显著差异，导致这些模型在对藏文对话型阅读理解的对话历史进行建模时存在困难。鉴于此，本文利用当前大模型的优越能力，提出了一种基于提示的对话历史建模方法--TicomR，以解决藏文对话型阅读理解任务中模型性能受限的问题。该方法通过引入基于提示的学习机制，直接在段落文本中添加提示来突显对话历史，而非修改段落标记嵌入，从而在微调过程中实现对对话历史的精确建模，以增强对模型对问题的理解能力。实验结果表明，TiComR模型在藏文对话型阅读理解任务上取得了显著的性能提升，并在英文数据集CoQA上也有较好的表现。

## 参数设置
我们对选取的基线模型的实验参数均遵循原始论文的最好设置，在此不做详细描述。对于TicomR的具体实验参数设置如下表所示，所有实验均在2张Tesla V100-PCIE-32G上完成。在表3中我们比较了基线模型在TiconvQA和CoQA上的结果。

| Parameters                          | Values     |
|-------------------------------------|------------|
| cutoff_len                          | 2048       |
| learning_rate                       | 2e-4       |
| num_tran_epochs                     | 2.0        |
| max_samples                         | 100000     |
| per_devices_train_batch_size        | 4          |
| gradient_accumulation_steps         | 4          |
| max_grad_norm                       | 1.0        |
| lora_rank                           | 8          |
| lora_dropout                        | 0.05       |
| resume_lora_training                | True       |

## 模型性能
本文选择DrQA、SDNet、TiBERT、TBERT等作为基线模型，以上前两者是英文领域经典模型，TiBERT、TBERT是现有常用的藏文预训练语言模型，它们在英文、藏文领域文本分类、情感分析等下游任务上有着出色的表现。具体实验结果下表所示。

（1）DrQA：DrQA是一种基于深度学习的问答模型，通过双向长短期记忆网络（BiLSTM）编码文档和问题，并结合注意力机制。其特点包括端到端的训练、支持多种问答任务、良好的扩展性和高效性，以及通过交互式学习进一步提高性能。

（2）SDNet：SDNet是一种用于端到端问答的神经模型，它通过联合学习问题理解、证据检索和答案生成的过程来提高性能。模型采用了一种层次化的注意力机制，首先对问题进行编码，然后从支持文档中检索相关信息，最后利用这些信息生成准确的答案。SDNet在多个问答数据集上进行了评估，显示出优于传统方法和现有神经模型的性能。

（3）TiBERT：TiBERT是针对藏语自然语言处理任务设计的预训练语言模型。它在大规模藏语训练数据上进行训练，利用Sentencepiece构建了能够覆盖大部分藏语单词的词汇库。TiBERT在文本分类和问题生成等下游任务上展现了出色的性能，并相比经典模型和多语言预训练模型具有优势。该模型的推出为藏语自然语言处理领域的发展提供了有力支持。

（4）TBERT：TBERT（Tibetan-BERT）模型是一种针对藏文自然语言处理任务设计的预训练语言模型。由青海师范大学省部共建藏语智能信息处理及应用国家重点实验室的多拉教授团队与兰州大学开源软件与实时系统教育部工程研究中心共同开发。TBERT旨在解决藏语在自然语言处理领域的数据资源限制和技术挑战，推动藏文信息处理技术的发展。模型基于BERT架构，使用SentencePiece分词器，适用于各种藏语NLP任务。

| Model     | TiconvQA F1 (%) | TiconvQA EM (%) | CoQA F1 (%) | CoQA EM (%) |
|-----------|------------------|-----------------|-------------|-------------|
| 人类表现  | 89.5             | 80.2            | 88.8        | -           |
| DrQA      | 66.5             | 44.6            | 55.6        | 46.2        |
| SDNet     | 46.2             | -               | 76.6        | -           |
| TiBERT    | 40.6             | 32.7            | -           | -           |
| TBERT     | 37.4             | 21.8            | -           | -           |
| TicomR    | 82.1             | 58.9            | 78.1        | 50.6        |

## 参考文献
[1]Chen D, Fisch A, Weston J, et al. Reading wikipedia to answer open-domain questions[J]. arXiv preprint arXiv:1704.00051, 2017.

[2]Zhu C, Zeng M, Huang X. Sdnet: Contextualized attention-based deep network for conversational question answering[J]. arXiv preprint arXiv:1812.03593, 2018.

[3]Liu S, Deng J, Sun Y, et al. Tibert: Tibetan pre-trained language model[C]//2022 IEEE International Conference on Systems, Man, and Cybernetics (SMC). IEEE, 2022: 2956-2961.

[4]https://github.com/TBNLP/TiconvQA

[5]https://github.com/NLP-Learning/TiLamb

[6]https://github.com/Dslab-NLP/Tibetan-PLM

[7]Zhao W X, Zhou K, Li J, et al. A survey of large language models[J]. arXiv preprint arXiv:2303.18223, 2023.

[8]Liu P, Yuan W, Fu J, et al. Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing[J]. ACM Computing Surveys, 2023, 55(9): 1-35.

...
