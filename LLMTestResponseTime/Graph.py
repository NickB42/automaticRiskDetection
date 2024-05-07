import matplotlib.pyplot as plt
import json

def readFromFile(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"Contents of '{filename}':")
        return(data)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")


models= ["gpt-35-turbo-16k", "gpt-4","gpt-4-32k","gpt-4-turbo","gcp-chat-bison-001","anthropic-claude-v2-100k","cohere-command","llama2-70b-chat-hf","ai21-j2-jumbo-instruct","alephalpha"]


results = readFromFile("NewResultsEnd.json")

plt.figure(figsize=(10, 6))

for model in models:
    model_results = [result for result in results if result[0] == model]    
    model_results = sorted(model_results,key=lambda x: x[1])

    model_tokens = [arr[1] for arr in model_results]
    model_times = [arr[2] for arr in model_results]
    
    plt.plot(model_tokens, model_times, label=model)

plt.xlabel('Anzahl der Output-Tokens')
plt.ylabel('Zeit (s)')
plt.title('Verarbeitungsdauer verschiedener LLMs in Abhängigkeit der generierten Output-Token')
plt.legend()
plt.tight_layout()
plt.show()