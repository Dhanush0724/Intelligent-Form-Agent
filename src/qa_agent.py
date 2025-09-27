from transformers import pipeline

class FormQA:
    def __init__(self):
        # Load question-answering pipeline
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    def answer_question(self, text, question):
        """
        text: string - extracted form text
        question: string - question to ask
        """
        result = self.qa_pipeline(question=question, context=text)
        return result['answer']
