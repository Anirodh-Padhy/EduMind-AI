import re

# ---------------------------------------------------
# PARSE QUIZ TEXT
# ---------------------------------------------------

def parse_quiz(quiz_text):

    questions = []

    blocks = quiz_text.split("Q:")

    for block in blocks[1:]:

        lines = block.strip().split("\n")

        if len(lines) < 6:

            continue

        question = lines[0]

        options = []

        answer = ""

        for line in lines[1:]:

            if line.startswith(("A)", "B)", "C)", "D)")):

                options.append(line)

            if line.startswith("Answer:"):

                answer = (
                    line.replace(
                        "Answer:",
                        ""
                    ).strip()
                )

        questions.append({

            "question": question,

            "options": options,

            "answer": answer
        })

    return questions