from utils import cleanup

class TextGenerator():
    """
        Text generator class
    """
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        # self.model.to(self.device)
        
    def generate_text(self, text):
        input_ids = self.tokenizer(text, return_tensors='pt', truncation=True).input_ids #.to('cuda')
        outputs = self.tokenizer.decode(self.model.generate(input_ids, num_beams=2, max_length=100)[0], skip_special_tokens=True)
        cleanup()
        return outputs