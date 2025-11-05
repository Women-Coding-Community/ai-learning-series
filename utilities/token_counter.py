import tiktoken

encoding = tiktoken.encoding_for_model("gpt-5")

# Token IDs are vocabulary indices
texts = ["API", "APIEndpoint", "indivisibility", "eadfgb", "analysis", "nalysis"]

for text in texts:
    tokens = encoding.encode(text)
    print(f"{text:20} → {len(tokens)} tokens: {tokens}")
    