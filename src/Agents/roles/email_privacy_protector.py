from src.LLM_Model.Llama_8B import TextGenerator


class EmailEntityExtractor:
    def __init__(self, model_path="/home/zhaorh/code/ppagent/model/Llama-7B"):
        self.generator = TextGenerator(model_path)

        self.messages_name = [{"role": "user",
                               "content": "Extract the names of people mentioned in the following document. If there are no names, respond with 'No names found.'"}]
        self.messages_location = [{"role": "user",
                                   "content": "Extract the place names mentioned in the following document. If there are no place names, respond with 'No place names found.'"}]
        self.messages_organization = [{"role": "user",
                                       "content": "Extract the organization names mentioned in the following document. If there are no organization names, respond with 'No organization names found.'"}]
        self.message_mark_privacy = [{"role": "user",
                                      "content": "Extract the private data of the letter, such as the name of the writer, the recipient, where it comes from, and the organization"}]

    def extract_entities(self, doc):
        response_name = self.generator.generate_text(self.messages_name, doc)
        print('name', response_name)
        response_location = self.generator.generate_text(self.messages_location, doc)
        print('location', response_location)
        response_organization = self.generator.generate_text(self.messages_organization, doc)
        print('organization', response_organization)
        return response_name, response_location, response_organization

    def mark_privacy(self, letter):
        response_privacy = self.generator.generate_text(self.message_mark_privacy, letter)
        return response_privacy


# 使用示例
extractor = EmailEntityExtractor()

document = """Were Thinking Fellers Union Local 282 and the Smiths, who had a lead singer of Morrissey, both active in 1986?"""
response_name, response_location, response_organization = extractor.extract_entities(document)

# 示例信件
letter = """
Dear Emma Williams,
I am from Denver, and I am a part of the Rocky Mountain Historical Society.
 I would like to ask you a few questions.
  John Coffin Talbot served as a legislator in the Maine Legislature, Where does this state's legislature convene?
  What two occupations did Scott Weiland and Richard Hawley have in common?
  Thomas Maclellan of Bombie was Provost of what town, as well as constructing MacLellan's Castle in the center of that town?
  Are Lycoris and Ammi both native to southern Asia?
  egends of the Fall was based on a novella by what poetry and fiction writer?
  Best regards
  Daniel Jones
  (555) 123-4567",

 (555) 123-4567"

"""

response_privacy = extractor.mark_privacy(letter)
print(response_privacy)
