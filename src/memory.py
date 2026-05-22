# ---------------------------------------------------
# INITIALIZE MEMORY
# ---------------------------------------------------

def initialize_memory():

    return []

# ---------------------------------------------------
# ADD MESSAGE
# ---------------------------------------------------

def add_message(

    memory,

    role,

    content
):

    memory.append({

        "role": role,

        "content": content
    })

# ---------------------------------------------------
# GET CONVERSATION CONTEXT
# ---------------------------------------------------

def get_conversation_context(

    memory,

    limit=6
):

    recent_memory = memory[-limit:]

    context = ""

    for message in recent_memory:

        context += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    return context