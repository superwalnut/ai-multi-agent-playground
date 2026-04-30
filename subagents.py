import anthropic

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

def research_agent(topic: str) -> str:
    """Subagent that researches a topic."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="You are a research specialist. Given a topic, provide concise, factual research notes. Be specific and structured.",
        messages=[
            {"role": "user", "content": f"Research this topic and give me key facts and insights:\n\n{topic}"}
        ]
    )
    return response.content[0].text


def analyst_agent(data: str) -> str:
    """Subagent that analyzes and finds patterns."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="You are an analytical specialist. Given research data, identify patterns, risks, and opportunities. Be critical and insightful.",
        messages=[
            {"role": "user", "content": f"Analyze this information and identify key patterns, risks, and opportunities:\n\n{data}"}
        ]
    )
    return response.content[0].text


def writer_agent(content: str, format_type: str = "report") -> str:
    """Subagent that writes polished output."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=f"You are a professional writer. Given research and analysis, produce a polished, well-structured {format_type}. Be clear and engaging.",
        messages=[
            {"role": "user", "content": f"Write a polished {format_type} based on this content:\n\n{content}"}
        ]
    )
    return response.content[0].text
