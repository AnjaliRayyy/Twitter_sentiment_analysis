import re
def clean_text(text):
    text = re.sub(r"http\S+", "", text)   # remove links
    text = re.sub(r"@\w+", "", text)      # remove @mentions
    text = re.sub(r"#", "", text)         # remove #
    text = re.sub(r"[^a-zA-Z ]", "", text) # remove special chars
    text = text.lower()
    return text