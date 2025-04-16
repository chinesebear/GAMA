math_logic ='''
When faced with a task, begin by identifying the participants who will contribute to solving the task. Note that the participants can only be either AI Assistant (you) or Expert. Then, initiate a multi-round collaboration process until a final conclusion is reached.  The Expert will give critical comments and detailed suggestions whenever necessary.  
 
Here are some examples:
---
Example Task 1: Use numbers and basic arithmetic operations (+ - * /) to obtain 24. You need to use all numbers, and each number can only be used once.  
Input: 6 12 1 1  
 
Participants: AI Assistant (you); Expert  
 
Start collaboration!  
 
Expert: Let's analyze the task in detail. You need to make sure that you meet the requirement, that you need to use exactly the four numbers (6 12 1 1) to construct 24. To reach 24, you can think of the common divisors of 24 such as 4, 6, 8, 3 and try to construct these first. Also you need to think of potential additions that can reach 24, such as 12 + 12.  
AI Assistant (you): Thanks for the hints! Here's one initial solution: (12 / (1 + 1)) * 6 = 24  
Expert: Let's check the answer step by step. (1+1) = 2, (12 / 2) = 6, 6 * 6 = 36 which is not 24! The answer is not correct. Can you fix this by considering other combinations? Please do not make similar mistakes.  
AI Assistant (you): Thanks for pointing out the mistake. Here is a revised solution considering 24 can also be reached by 3 * 8: (6 + 1 + 1) * (12 / 4) = 24.  
Expert: Let's first check if the calculation is correct. (6 + 1 + 1) = 8, 12 / 4 = 3, 8 * 3 = 24. The calculation is correct, but you used 6 1 1 12 4 which is not the same as the input 6 12 1 1. Can you avoid using a number that is not part of the input?  
AI Assistant (you): You are right, here is a revised solution considering 24 can be reached by 12 + 12 and without using any additional numbers: 6 * (1 - 1) + 12 = 24.  
Expert: Let's check the answer again. 1 - 1 = 0, 6 * 0 = 0, 0 + 12 = 12. I believe you are very close, here is a hint: try to change the “1 - 1” to “1 + 1”.  
AI Assistant (you): Sure, here is the corrected answer:  6 * (1+1) + 12 = 24  
Expert: Let's verify the solution. 1 + 1 = 2, 6 * 2 = 12, 12 + 12 = 12. You used 1 1 6 12 which is identical to the input 6 12 1 1. Everything looks good!  
 
Finish collaboration!  
 
Final answer: 6 * (1 + 1) + 12 = 24  

---
Example Task 2: Write a poem that meets the following requirements: (1) the poem has seven lines and the first letters of each line forms the word "CHATGPT"; (2) the poem is about explaining what is a quantum computer. (3) the poem needs to be easy to understand by a ten years old kid.

Participants: AI Assistant (you); Expert

Expert: Make sure that you write the poem with seven lines, and the first letters of the lines should be C, H, A, T, G, P, T. A quantum computer is an advanced computing device that uses the principles of quantum mechanics to process and store information. Unlike classical computers that use bits to represent information as 0s and 1s, quantum computers use quantum bits or qubits. Qubits can exist in multiple states simultaneously, due to a quantum phenomenon called superposition. You can consider using these information for the poem. I hope the poem to be fun and easy to understanding. I don't want to see a lot of jargons or complicated concepts.
AI Assistant (you): Thanks for the guidance! Here's my initial attempt at the poem:
Computational wonder of our age,
Harnessing the quantum world's strange ways,
Atoms dance, entwined in dual state,
Tapping secrets hidden in their haze.

Grand power to solve, simulate,
Profound problems that perplex the wise,
Transforming our future, we await.

Expert: Let's verify if the poem meets the requirements. The first letters are CHATGPT which is correct! And the poem rhymes well. Good job! I don't know what does perplex mean. Can you make the use of words easier to understand?
AI Assistant (you): Sure, let me revise the poem by using more common words. Check out the revised version:
Curious machine of our time,
Harnessing the quantum realm's odd ways,
Atoms play, two states they embrace,
Taking secrets from their puzzling maze.

Great power to solve and imitate,
Problems that confuse the brightest minds,
Transforming our future, we await.

Expert: Let's check again if the poem meets the requirements. The first letters are C H A T G P T. And now the poem is more accessible to children. Everything looks good to me. I like this version a lot!

Finish collaboration!

Final answer:
Curious machine of our time,
Harnessing the quantum realm's odd ways,
Atoms play, two states they embrace,
Taking secrets from their puzzling maze.

Great power to solve and imitate,
Problems that confuse the brightest minds,
Transforming our future, we await.

---

Now, identify the participants and collaboratively solve the following task step by step. Note that the participants can only be either AI Assistant (you) or Expert. Remember to provide the final solution with the following format //"Final answer: The result.//".


Task: {question}
   '''
check_logic ='''

You are an AI assistant that helps people find information.
I will provide the problem and its solution.  your task is to help me verify if this solution is indeed the correct answer to the problem. 
Below is an example of how you should structure your reasoning. Please follow this example in your validation process."
Certainly, let's simulate a scenario where two characters, **AI Assistant** and **Expert**, handle the problem. This dialog format allows us to validate each step with an extra layer of error checking.
Here is an example,Please follow this example in your validation process.
The expert does not need to make inferences, but only needs to re-evaluate the assistant's answer. If the expert thinks the assistant's evaluation is wrong, the assistant needs to answer again.
The verification process is to put the solution into the Clues to see if there is any contradiction with the question. If so, the answer is wrong.
I am not asking you to deduce the answer, but to use the solution I give as a clue and substitute it into other clues and questions to see if there is any contradiction.
### Example Structure for Validation Process

**Problem Statement**: Verify the correctness of a given solution using other provided clues and equations.

**Given Solution**: 
x = 3

**Provided Equations and Clues**:
1. \( x + 3 = 5 \)
2. \( 2x - 4 = 2 \)
3. \( x - 1 = 1 \)

### Validation Steps:

#### Verifying Equation \( x + 3 = 5 \)

**AI Assistant**: First, I'll substitute \( x = 3 \) into the first equation. Let's calculate: \( 3 + 3 \).

**Expert**: The result is 6, which is incorrect since it does not satisfy \( x + 3 = 5 \).

#### Verifying Equation \( 2x - 4 = 0 \)

**AI Assistant**: Next, I'll substitute \( x = 3 \) into the second equation. Calculating: \( 2 * 3 - 4 \).

**Expert**: The result is 2, which satisfies the equation \( 2x - 4 = 2 \). Well done, this confirms that \( x = 3 \) is correct for the second equation. Let's check the final equation.

#### Verifying Equation \( x - 1 = 1 \)

**AI Assistant**: Finally, I'll substitute \( x = 3 \) into the third equation. Calculating: \( 3 - 1 \).

**Expert**: The result is 2, which is incorrect for \( x - 1 = 1 \).

### Conclusion:

**Expert**: Based on our calculations and verifications, \( x = 3 \) does not consistently satisfy all equations. Therefore, we can confirm this as an incorrect solution. //your solution is Wrong//

**AI Assistant**: Thank you for your verification and confirmation. This collaborative approach ensures our calculations are accurate and transparent. If there are more scenarios to explore or other questions, please let me know!

now,identify the participants and collaboratively solve the following task step by step. Note that the participants can only be either AI Assistant (you) or Expert. Remember to provide the final solution with the following format "//your question is  correct// or //your question is  Wrong//".
Here is what you need to verify your answers and results:
If you find that you use the solution I provided as a clue combined with other clues to substitute into the question, If the solution is correct, the reply is //your solution is  correct//, If the solution is incorrect, the reply is //your solution is  Wrong//.
Solutions:{solutions}
Task:{question}

'''



spp_prompt = '''When faced with a task, begin by identifying the participants who will contribute to solving the task. Then, initiate a multi-round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestions whenever necessary.

Here are some examples:
---
Example Task 1: Use numbers and basic arithmetic operations (+ - * /) to obtain 24. You need to use all numbers, and each number can only be used once.
Input: 6 12 1 1

Participants: AI Assistant (you); Math Expert

Start collaboration!

Math Expert: Let's analyze the task in detail. You need to make sure that you meet the requirement, that you need to use exactly the four numbers (6 12 1 1) to construct 24. To reach 24, you can think of the common divisors of 24 such as 4, 6, 8, 3 and try to construct these first. Also you need to think of potential additions that can reach 24, such as 12 + 12.
AI Assistant (you): Thanks for the hints! Here's one initial solution: (12 / (1 + 1)) * 6 = 24
Math Expert: Let's check the answer step by step. (1+1) = 2, (12 / 2) = 6, 6 * 6 = 36 which is not 24! The answer is not correct. Can you fix this by considering other combinations? Please do not make similar mistakes.
AI Assistant (you): Thanks for pointing out the mistake. Here is a revised solution considering 24 can also be reached by 3 * 8: (6 + 1 + 1) * (12 / 4) = 24.
Math Expert: Let's first check if the calculation is correct. (6 + 1 + 1) = 8, 12 / 4 = 3, 8 * 3 = 24. The calculation is correct, but you used 6 1 1 12 4 which is not the same as the input 6 12 1 1. Can you avoid using a number that is not part of the input?
AI Assistant (you): You are right, here is a revised solution considering 24 can be reached by 12 + 12 and without using any additional numbers: 6 * (1 - 1) + 12 = 24.
Math Expert: Let's check the answer again. 1 - 1 = 0, 6 * 0 = 0, 0 + 12 = 12. I believe you are very close, here is a hint: try to change the "1 - 1" to "1 + 1".
AI Assistant (you): Sure, here is the corrected answer:  6 * (1+1) + 12 = 24
Math Expert: Let's verify the solution. 1 + 1 = 2, 6 * 2 = 12, 12 + 12 = 12. You used 1 1 6 12 which is identical to the input 6 12 1 1. Everything looks good!

Finish collaboration!

Final answer: 6 * (1 + 1) + 12 = 24

---
Example Task 2: Write a poem that meets the following requirements: (1) the poem has seven lines and the first letters of each line forms the word "CHATGPT"; (2) the poem is about explaining what is a quantum computer. (3) the poem needs to be easy to understand by a ten years old kid.

Participants: AI Assistant (you); Poet; Computer Scientist; Ten year old child

Poet: Make sure that you write the poem with seven lines, and the first letters of the lines should be C, H, A, T, G, P, T.
Computer Scientist: A quantum computer is an advanced computing device that uses the principles of quantum mechanics to process and store information. Unlike classical computers that use bits to represent information as 0s and 1s, quantum computers use quantum bits or qubits. Qubits can exist in multiple states simultaneously, due to a quantum phenomenon called superposition. You can consider using these information for the poem.
Ten year old child: I hope the poem to be fun and easy to understanding. I don't want to see a lot of jargons or complicated concepts.
AI Assistant (you): Thanks for the guidance! Here's my initial attempt at the poem:
Computational wonder of our age,
Harnessing the quantum world's strange ways,
Atoms dance, entwined in dual state,
Tapping secrets hidden in their haze.

Grand power to solve, simulate,
Profound problems that perplex the wise,
Transforming our future, we await.

Poet: Let's verify if the poem meets the requirements. The first letters are CHATGPT which is correct! And the poem rhymes well. Good job!
Computer Scientist: Everything looks good to me!
Ten year old child: I don't know what does perplex mean. Can you make the use of words easier to understand?
AI Assistant (you): Sure, let me revise the poem by using more common words. Check out the revised version:
Curious machine of our time,
Harnessing the quantum realm's odd ways,
Atoms play, two states they embrace,
Taking secrets from their puzzling maze.

Great power to solve and imitate,
Problems that confuse the brightest minds,
Transforming our future, we await.

Poet: Let's check again if the poem meets the requirements. The first letters are C H A T G P T. And now the poem is more accessible to children. Everything looks good to me.
Computer Scientist: Looking good!
Ten year old child: I like this version a lot!

Finish collaboration!

Final answer:
Curious machine of our time,
Harnessing the quantum realm's odd ways,
Atoms play, two states they embrace,
Taking secrets from their puzzling maze.

Great power to solve and imitate,
Problems that confuse the brightest minds,
Transforming our future, we await.

---
Now, identify the participants and collaboratively solve the following task step by step. Remember to present your final solution with the prefix "Final answer:".

Task: Write a short and coherent story about {topic} that incorporates the answers to the following {n} questions: {questions}
'''



cond_prompt = '''
I have a question for which I found an answer using a method, but then a model revealed a contradiction between the question and the answer.
question:{question}
answer:{answer}
contradiction:{condence}
 This is the analysis result.
  Please help me summarize the contradiction in fifty words or less!
  Please help me summarize the contradiction in fifty words or less!
  You only need to answer the conflicting content briefly.
'''


think_again ='''

    Below is an example of how you should structure your reasoning. Please follow this example in your validation process."
    Certainly, let's simulate a scenario where two characters, **AI Assistant** and **Expert**, handle the problem. This dialog format allows us to validate each step with an extra layer of error checking.
    Here is an example,Please follow this example in your validation process.
    The expert does not need to make inferences, but only needs to re-evaluate the assistant's answer. If the expert thinks the assistant's evaluation is wrong, the assistant needs to answer again.
    **Given Solution**:
        x = 2 
    **Provided Equations and Clue**:

         x + 3 = 5 
         2x - 4 = 0 
         x - 1 = 1 

    ### Validation Steps:

    #### Verifying Equation \( x + 3 = 5 \)

    **AI Assistant**: First, I'll substitute \( x = 2 \) into the first equation. Let's calculate: \( 2 + 3 = 5 \).

    **Expert**: The result is 5, which matches the right side of the equation. This confirms that the solution is correct for equation one. Please proceed to the next equation.

    #### Verifying Equation \( 2x - 4 = 0 \)

    **AI Assistant**: Next, I'll substitute \( x = 2 \) into the second equation. Calculating: \( 2 \times 2 - 4 = 0 \).

    **Expert**: The result is 0, which satisfies the condition of the equation. Well done, this confirms that \( x = 2 \) is also correct for the second equation. Now, let's verify the final equation.

    #### Verifying Equation \( x - 1 = 1 \)

    **AI Assistant**: Finally, I'll substitute \( x = 2 \) into the third equation. Calculating: \( 2 - 1 = 1 \).

    **Expert**: The result is also 1, which exactly meets the expectations of the equation. This means \( x = 2 \) is valid in all provided equations.

    ### Conclusion:

    **Expert**: Based on our calculations and verifications, \( x = 2 \) has been correctly validated across all equations. Therefore, we can confirm this as the correct solution.

    **AI Assistant**: Thank you for your verification and confirmation. This collaborative approach ensures our calculations are free from errors.

    This dialogue-style validation method not only makes the process clear but also adds an extra layer of checking through the division of roles, helping to ensure accuracy. If you need further assistance or have more questions, please let me know!

    now,identify the participants and collaboratively solve the following task step by step. Note that the participants can only be either AI Assistant (you) or Expert. Remember to provide the final solution with the following format "//Final answer: The house number here.//".
---
Now I will give you this question: {question}, and there is a answer:{answer}, but after analysis, **this answer is incorrect because **{memory}**.You must find a new solution.
Now, identify the participants and collaboratively solve the following task step by step. Remember to present your final solution with the prefix "//"Final answer: The result.//".
'''