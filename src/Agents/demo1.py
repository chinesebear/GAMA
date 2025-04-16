import asyncio  # Import asyncio for running asynchronous code

from src.Agents.roles.sub_q_check import SubCheckMan


async def main():
    a_question = 'Who was the youngest brother in the Beach Boys?'
    max_iterations = 4  # Maximum loop iterations
    iterations = 0  # Counter initialization
    check_result_man = SubCheckMan()  # Instantiate the SubCheckMan class
    contradictions = True  # Initialize contradictions flag
    result = 'None'  # Starting result

    while contradictions and iterations < max_iterations:
        # Check if the result is correct using the check method
        check_result = await check_result_man.check(a_question, result)

        if isinstance(check_result, tuple) and len(check_result) == 2:
            # If the check returns a tuple, evaluate the result
            contradictions = not check_result[0]  # Set contradictions based on check_result[0]
            result = check_result[1]  # Update the result
        elif isinstance(check_result, bool):
            # If the check returns a boolean, set contradictions based on its value
            contradictions = not check_result  # Set contradictions based on check_result
            if contradictions:
                result = "No answer found"  # Set default result if no valid answer is found
        else:
            # Handle unexpected result format
            contradictions = True
            result = "Unexpected result format"

        # Update iterations and print current state
        iterations += 1
        print(f"Contradictions: {contradictions}")
        print(f"Result: {result}")


# Run the async main function using asyncio
asyncio.run(main())
