from .llm_engine import ask_llm

def synthesize_across_docs(context: str, query: str):
    """
    Generates a detailed, structured synthesis of the retrieved context.
    The model is free to choose paragraphs, lists, or subsections naturally.
    """
    prompt = f"""
You are an expert AI researcher writing a literature-based analysis.

Use the information below to answer the question comprehensively and clearly.

Context:
{context}

Question:
{query}

Guidelines:
- Write in an academic, explanatory tone.
- You may use paragraphs, bullet points, or numbered lists **only where appropriate**.
- Organize your thoughts logically (e.g., Introduction, Comparison, Insights, Future Directions).
- Be as detailed as needed, but stay focused on what the documents actually imply.
- Do **not** apologize or mention lacking information — focus on what's available.

Now provide your full answer:
"""
    return ask_llm(prompt)
