import ollama

# ---------------------------------------------------
# AI TUTOR RESPONSE
# ---------------------------------------------------

def generate_ai_response(

    user_prompt,

    conversation_context=""
):

    try:

        full_prompt = f"""

        You are EduMind AI,
        an advanced AI tutor.

        Your job:
        - teach concepts clearly
        - explain step-by-step
        - help students learn
        - provide simple examples
        - encourage learning

        Keep explanations:
        - beginner friendly
        - concise
        - educational
        - structured

        ---------------------------------------------------

        CONVERSATION HISTORY:
        {conversation_context}

        ---------------------------------------------------

        STUDENT QUESTION:
        {user_prompt}
        """

        response = ollama.chat(

            model="phi3",

            messages=[

                {
                    "role": "system",

                    "content":
                    """
                    You are an AI education tutor.
                    """
                },

                {
                    "role": "user",

                    "content": full_prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"