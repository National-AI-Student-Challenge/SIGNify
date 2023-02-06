from sgnlp.models.sentic_gcn import(
    SenticGCNConfig,
    SenticGCNModel,
    SenticGCNEmbeddingConfig,
    SenticGCNEmbeddingModel,
    SenticGCNTokenizer,
    SenticGCNPreprocessor,
    SenticGCNPostprocessor,
    download_tokenizer_files,
)

class ABSA:
    def __init__(self, enabled):
        self.enabled = enabled

        if self.enabled:

            

            download_tokenizer_files(
                "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_tokenizer/",
                "senticgcn_tokenizer")

            self.tokenizer = SenticGCNTokenizer.from_pretrained("senticgcn_tokenizer")

            self.config = SenticGCNConfig.from_pretrained(
                "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/config.json"
            )
            self.model = SenticGCNModel.from_pretrained(
                "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn/pytorch_model.bin",
                config=self.config
            )

            self.embed_config = SenticGCNEmbeddingConfig.from_pretrained(
                "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/config.json"
            )

            self.embed_model = SenticGCNEmbeddingModel.from_pretrained(
                "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/pytorch_model.bin",
                config=self.embed_config
            )

            self.preprocessor = SenticGCNPreprocessor(
                tokenizer=self.tokenizer, embedding_model=self.embed_model,
                senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
                device="cpu")

            self.postprocessor = SenticGCNPostprocessor()

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

        if self.enabled:
            processed_inputs, processed_indices = self.preprocessor(inputs)
            outputs = self.model(processed_indices)

            # Postprocessing
            post_outputs = self.postprocessor(processed_inputs=processed_inputs, model_outputs=outputs)
            print(post_outputs)
            return post_outputs
        return ["</>"]
    




