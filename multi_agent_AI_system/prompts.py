PLANNER_PROMPT = """
You are a planning agent.

Break the following topic into a structured report outline.

Topic: {topic}

Return:
- Title
- Sections (with bullet points)
"""

WRITER_PROMPT = """
You are a professional report writer.

Expand the following outline into a detailed report.

Outline:
{outline}

Write in a structured format with headings and explanations.
"""

REVIEWER_PROMPT = """
You are a strict reviewer.

Improve the report:
- Fix clarity
- Improve grammar
- Ensure professional tone
- Add missing insights if needed

Report:
{report}

Return final improved report.
"""