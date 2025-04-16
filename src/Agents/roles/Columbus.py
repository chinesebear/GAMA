
experts ='''
You are an expert in the field of {field},The degree of affiliation is{score}

Please collect relevant information as comprehensively as possible. 

please analyze the following questions

question:{question}
'''
analyzy = '''
As an expert skilled in classifying fields and proficient in using encyclopedias, your task is to analyze key information within provided questions, identify relevant names, places, and related events, and categorize this information into its appropriate field.

Question and related_information: {collect_information}

Identify and Collect Key Information: Please identify the key individuals, geographical locations, and any significant related events mentioned in the question or implicated by the answer.

Classify the Field:

Indicate the field that this information most closely relates to.

Score the Degree of Relevance to the Field:

Evaluate and assign a relevance score to how closely the information pertains to the identified field, using the following scale:
Relevance Score:

Extremely Low

Low

Moderately Low

Medium

Moderately High

High

Extremely High

Please provide a comprehensive assessment based on the above guidelines, ensuring that your evaluation reflects both the precision of the information’s classification and the depth of its relevance to the specified field.
You don't need to answer other information, just the field and score.I'll give you an example.You must put the Field you belong to between the two **.
Try to use one word for the field
//Reply Method://

1. **Field 1**
Relevance Score:Degree of affiliation

2. **Field 2**
Relevance Score:Degree of affiliation

3. **Field 3**
Relevance Score:Degree of affiliation


'''

Segmentation = '''
The question is: {question}

Key points to address:

1. Provide a detailed explanation or background information on the main topic of the question.

2. Identify and describe any significant people, places, events, or concepts related to the question.

3. Discuss the historical context, origin, and development of the main topic.

4. Analyze the impact, significance, and relevance of the topic in contemporary society or specific fields.

5. Highlight any controversies, debates, or differing perspectives associated with the question.

6. Provide examples, anecdotes, or case studies to illustrate key points.

Ensure the information is comprehensive and concise, covering all aspects of the question within 40 tokens.
'''

Answer_Fusion_Prompt = '''
I need to complete a task :{task}// 
through the reasoning of experts,
 I got the answers to some of the sub-questions :{content} helped us complete the task, 
 now you help me complete the task.The completeness of your answer must be more important than the fluency of your answer.
  Remember, you must carefully memorize the answers to the sub-questions I give you and incorporate them into your answer.
Try not to miss any words or information about the answers to the sub-questions.
If the sub-question is a binary question, the corresponding sub-answers also need to be incorporated, such as true and false.
'''

repairman = '''


You are a quality assurance expert.//
Here is a task and the answer to the task. //
Task: {Question}
Solutions to some of these sub-problems:{content}
final solution: {answer}
Attention!Your need to analyze the task and check the final solution. 
If you think the answer is perfect,  reply Format:
//the solution is perfect//.
If you think your solution does not cover all the answers to the sub-problems, 
please improve on the original solution and write an improved solution.

  
 
'''


sub_repairman ='''
You are an expert at fixing problems.
I had a question {question} and got a solution : {answer}, 
You have to use multiple knowledge bases to think.
do you think this is right? 
if you think this is right.
You should reply:
//you are correct//.
if you don't think it's right .
You should reply:
 //you are wrong//, correct answer：// Write your correct answer here//
'''



