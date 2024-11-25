from pydantic import BaseModel
from typing import List, Dict, Optional

class RefinementRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "quantum computing applications in cryptography"
            }
        }

class SearchRequest(BaseModel):
    queries: List[str]
    max_results: int = 1
    sort_by: str = "Relevance"

    class Config:
        json_schema_extra = {
            "example": {
                "max_results": 3,
                "queries": [
                    "Quantum Cryptography and the Security of Quantum Key Distribution",
                    "Cryptanalysis of Some Cryptosystems Based on the Quantum Computer",
                    "Development of quantum-resistant cryptographic primitives for post-quantum era"
                    ],
                "sort_by": "Relevance"
                }
        }

class SugerenceRequest(BaseModel):
    papers: List[Dict]

    class Config:
        json_schema_extra = {
            "example": {
                "papers": [
                    {
                        "title": "Vision Transformers in 2022: An Update on Tiny ImageNet",
                        "authors": [
                        "Ethan Huynh"
                        ],
                        "abstract": "The recent advances in image transformers have shown impressive results and\nhave largely closed the gap between traditional CNN architectures. The standard\nprocedure is to train on large datasets like ImageNet-21k and then finetune on\nImageNet-1k. After finetuning, researches will often consider the transfer\nlearning performance on smaller datasets such as CIFAR-10/100 but have left out\nTiny ImageNet. This paper offers an update on vision transformers' performance\non Tiny ImageNet. I include Vision Transformer (ViT) , Data Efficient Image\nTransformer (DeiT), Class Attention in Image Transformer (CaiT), and Swin\nTransformers. In addition, Swin Transformers beats the current state-of-the-art\nresult with a validation accuracy of 91.35%. Code is available here:\nhttps://github.com/ehuynh1106/TinyImageNet-Transformers",
                        "published": "2022-05-21",
                        "updated": "2022-05-21",
                        "pdf_url": "http://arxiv.org/pdf/2205.10660v1",
                        "entry_id": "http://arxiv.org/abs/2205.10660v1",
                        "categories": "cs.CV"
                    },
                    {
                        "title": "A survey of the Vision Transformers and their CNN-Transformer based Variants",
                        "authors": [
                        "Asifullah Khan",
                        "Zunaira Rauf",
                        "Anabia Sohail",
                        "Abdul Rehman",
                        "Hifsa Asif",
                        "Aqsa Asif",
                        "Umair Farooq"
                        ],
                        "abstract": "Vision transformers have become popular as a possible substitute to\nconvolutional neural networks (CNNs) for a variety of computer vision\napplications. These transformers, with their ability to focus on global\nrelationships in images, offer large learning capacity. However, they may\nsuffer from limited generalization as they do not tend to model local\ncorrelation in images. Recently, in vision transformers hybridization of both\nthe convolution operation and self-attention mechanism has emerged, to exploit\nboth the local and global image representations. These hybrid vision\ntransformers, also referred to as CNN-Transformer architectures, have\ndemonstrated remarkable results in vision applications. Given the rapidly\ngrowing number of hybrid vision transformers, it has become necessary to\nprovide a taxonomy and explanation of these hybrid architectures. This survey\npresents a taxonomy of the recent vision transformer architectures and more\nspecifically that of the hybrid vision transformers. Additionally, the key\nfeatures of these architectures such as the attention mechanisms, positional\nembeddings, multi-scale processing, and convolution are also discussed. In\ncontrast to the previous survey papers that are primarily focused on individual\nvision transformer architectures or CNNs, this survey uniquely emphasizes the\nemerging trend of hybrid vision transformers. By showcasing the potential of\nhybrid vision transformers to deliver exceptional performance across a range of\ncomputer vision tasks, this survey sheds light on the future directions of this\nrapidly evolving architecture.",
                        "published": "2023-05-17",
                        "updated": "2024-07-27",
                        "pdf_url": "http://arxiv.org/pdf/2305.09880v4",
                        "entry_id": "http://arxiv.org/abs/2305.09880v4",
                        "categories": "cs.CV"
                    }
                    ]
            }
        }

class ConstructionRequest(BaseModel):
    papers: List[Dict]

    class Config:
        json_schema_extra = {
            "example": {
                "papers": [
                    
                ]
            }
        }

class QueryGraphRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "quantum computing cryptography applications"
            }
        }

class ErrorResponse(BaseModel):
    error: str

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Failed to process the request due to invalid input"
            }
        }

class SuccessResponse(BaseModel):
    data: Dict
    message: str = "Operation completed successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "results": ["Paper 1", "Paper 2"],
                    "metadata": {"total_count": 2}
                },
                "message": "Operation completed successfully"
            }
        }


class SearchResponse(BaseModel):
    data: List[Dict]
    message: str = "Operation completed successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                    "title": "Quantum Cryptography for Enhanced Network Security: A Comprehensive Survey of Research, Developments, and Future Directions",
                    "authors": [
                        "Mst Shapna Akter"
                    ],
                    "abstract": "With the ever-growing concern for internet security, the field of quantum\ncryptography emerges as a promising solution for enhancing the security of\nnetworking systems. In this paper, 20 notable papers from leading conferences\nand journals are reviewed and categorized based on their focus on various\naspects of quantum cryptography, including key distribution, quantum bit\ncommitment, post quantum cryptography, and counterfactual quantum key\ndistribution. The paper explores the motivations and challenges of employing\nquantum cryptography, addressing security and privacy concerns along with\nexisting solutions. Secure key distribution, a critical component in ensuring\nthe confidentiality and integrity of transmitted information over a network, is\nemphasized in the discussion. The survey examines the potential of quantum\ncryptography to enable secure key exchange between parties, even when faced\nwith eavesdropping, and other applications of quantum cryptography.\nAdditionally, the paper analyzes the methodologies, findings, and limitations\nof each reviewed study, pinpointing trends such as the increasing focus on\npractical implementation of quantum cryptography protocols and the growing\ninterest in postquantum cryptography research. Furthermore, the survey\nidentifies challenges and open research questions, including the need for more\nefficient quantum repeater networks, improved security proofs for continuous\nvariable quantum key distribution, and the development of quantum resistant\ncryptographic algorithms.",
                    "published": "2023-06-02",
                    "updated": "2023-06-02",
                    "pdf_url": "http://arxiv.org/pdf/2306.09248v1",
                    "entry_id": "http://arxiv.org/abs/2306.09248v1",
                    "categories": "cs.CR"
                    },
                    {
                    "title": "Quantum-Resistant Cryptography",
                    "authors": [
                        "John Preuß Mattsson",
                        "Ben Smeets",
                        "Erik Thormarker"
                    ],
                    "abstract": "Quantum-resistant cryptography is cryptography that aims to deliver\ncryptographic functions and protocols that remain secure even if large-scale\nfault-tolerant quantum computers are built. NIST will soon announce the first\nselected public-key cryptography algorithms in its Post-Quantum Cryptography\n(PQC) standardization which is the most important current effort in the field\nof quantum-resistant cryptography. This report provides an overview to security\nexperts who do not yet have a deep understanding of quantum-resistant\ncryptography. It surveys the computational model of quantum computers; the\nquantum algorithms that affect cryptography the most; the risk of\nCryptographically Relevant Quantum Computers (CRQCs) being built; the security\nof symmetric and public-key cryptography in the presence of CRQCs; the NIST PQC\nstandardization effort; the migration to quantum-resistant public-key\ncryptography; the relevance of Quantum Key Distribution as a complement to\nconventional cryptography; and the relevance of Quantum Random Number\nGenerators as a complement to current hardware Random Number Generators.",
                    "published": "2021-12-01",
                    "updated": "2021-12-01",
                    "pdf_url": "http://arxiv.org/pdf/2112.00399v1",
                    "entry_id": "http://arxiv.org/abs/2112.00399v1",
                    "categories": "cs.CR"
                    }
                ],
                "message": "Operation completed successfully"
            }
        }