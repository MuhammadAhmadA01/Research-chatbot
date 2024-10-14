import re

with open("uncleaned.txt", "r", encoding="utf-8") as file:
    content = file.read()

pattern = r"(?:\d+|(?:\[\d+\]))"
paragraphs = content.split("\n\n")
cleaned_paragraphs = []

for paragraph in paragraphs:
    cleaned_paragraph = re.sub(pattern, "", paragraph)
    cleaned_paragraph = re.sub(r'[^\w\s]', '', cleaned_paragraph)
    cleaned_paragraphs.append(cleaned_paragraph)

with open("cleaned.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n\n".join(cleaned_paragraphs))

print("Cleaned paragraphs have been written to 'cleaned_paragraphs.txt'")