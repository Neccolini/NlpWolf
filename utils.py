import re
def extract_agent_int(context: str) -> int:
    pattern = r".*Agent\[0(\d)\].*"
    result = re.match(pattern, context)
    if result:
        return int(result.group(1))
    return 0