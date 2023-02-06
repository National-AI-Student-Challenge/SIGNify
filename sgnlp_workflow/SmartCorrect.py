## Link: https://sgnlp.aisingapore.net/grammatical-error-correction

from sgnlp.models.csgec import (
    CsgConfig,
    CsgModel,
    CsgTokenizer,
    CsgecPreprocessor,
    CsgecPostprocessor,
    download_tokenizer_files,
)

import os
import shutil

class SmartCorrect:
    def __init__(self, enabled):
        self.enabled = enabled
        if self.enabled:
            self.config = CsgConfig.from_pretrained("https://storage.googleapis.com/sgnlp/models/csgec/config.json")
            self.model = CsgModel.from_pretrained(
                "https://storage.googleapis.com/sgnlp/models/csgec/pytorch_model.bin",
                config=self.config,
            )

            for f in ['csgec_src_tokenizer','csgec_ctx_tokenizer','csgec_tgt_tokenizer']:
                if os.path.exists(f):
                    shutil.rmtree(f)

            download_tokenizer_files(
                "https://storage.googleapis.com/sgnlp/models/csgec/src_tokenizer/",
                "csgec_src_tokenizer",
            )
            download_tokenizer_files(
                "https://storage.googleapis.com/sgnlp/models/csgec/ctx_tokenizer/",
                "csgec_ctx_tokenizer",
            )
            download_tokenizer_files(
                "https://storage.googleapis.com/sgnlp/models/csgec/tgt_tokenizer/",
                "csgec_tgt_tokenizer",
            )


            
            self.src_tokenizer = CsgTokenizer.from_pretrained("csgec_src_tokenizer")
            self.ctx_tokenizer = CsgTokenizer.from_pretrained("csgec_ctx_tokenizer")
            self.tgt_tokenizer = CsgTokenizer.from_pretrained("csgec_tgt_tokenizer")

            self.preprocessor = CsgecPreprocessor(src_tokenizer=self.src_tokenizer, ctx_tokenizer=self.ctx_tokenizer)
            self.postprocessor = CsgecPostprocessor(tgt_tokenizer=self.tgt_tokenizer)

    def run(self,texts):
        if self.enabled:
            batch_source_ids, batch_context_ids = self.preprocessor(texts)
            predicted_ids = self.model.decode(batch_source_ids, batch_context_ids)
            predicted_texts = self.postprocessor(predicted_ids)
            return predicted_texts
        return [text + "..." for text in texts]
