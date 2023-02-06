from sgnlp.models.sentic_gcn import (
    SenticGCNBertTokenizer,
    SenticGCNBertEmbeddingConfig,
    SenticGCNBertEmbeddingModel,
    SenticGCNBertModel,
    SenticGCNBertPreprocessor,
    SenticGCNBertConfig,
    SenticGCNBertPostprocessor,
)

class ABSA:
    def __init__(self):
        # Create tokenizer
        self.tokenizer = SenticGCNBertTokenizer.from_pretrained("bert-base-uncased")

        # Create embedding model
        self.embed_config = SenticGCNBertEmbeddingConfig.from_pretrained("bert-base-uncased")
        self.embed_model = SenticGCNBertEmbeddingModel.from_pretrained("bert-base-uncased", config=self.embed_config)

        # Create preprocessor
        self.preprocessor = SenticGCNBertPreprocessor(
            tokenizer=self.tokenizer,
            embedding_model=self.embed_model,
            senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
            device="cpu",
        )

        # Create postprocessor
        self.postprocessor = SenticGCNBertPostprocessor()

        # Load model
        self.config = SenticGCNBertConfig.from_pretrained(
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/config.json"
        )

        self.model = SenticGCNBertModel.from_pretrained(
            "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_bert/pytorch_model.bin", config=self.config
        )

    def run(self, inputs):
        '''
        example inputs:
        [
            {  # Single word aspect
                "aspects": ["service"],
                "sentence": "To sum it up : service varies from good to mediorce , depending on which waiter you get ; generally it is just average ok .",
            },
            {  # Single-word, multiple aspects
                "aspects": ["service", "decor"],
                "sentence": "Everything is always cooked to perfection , the service is excellent, the decor cool and understated.",
            },
            {  # Multi-word aspect
                "aspects": ["grilled chicken", "chicken"],
                "sentence": "the only chicken i moderately enjoyed was their grilled chicken special with edamame puree .",
            },
        ]
        '''
        processed_inputs, processed_indices = self.preprocessor(inputs)
        outputs = self.model(processed_indices)

        # Postprocessing
        post_outputs = self.postprocessor(processed_inputs=processed_inputs, model_outputs=outputs)
        return post_outputs





