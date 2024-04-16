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


models= ["gpt-35-turbo-16k", "gpt-4","gpt-4-32k","gpt-4-turbo","cohere-command","gcp-chat-bison-001","anthropic-claude-v2-100k","alephalpha","ai21-j2-jumbo-instruct","llama2-70b-chat-hf"]

newRes = [['gpt-35-turbo-16k', 7, 1.3475, 0.1925], ['gpt-35-turbo-16k', 22, 0.99606, 0.04528], ['gpt-35-turbo-16k', 72, 1.66189, 0.02308], ['gpt-35-turbo-16k', 94, 2.2586, 0.02403], ['gpt-35-turbo-16k', 344, 5.72202, 0.01663], ['gpt-35-turbo-16k', 120, 2.45348, 0.02045], ['gpt-35-turbo-16k', 133, 2.4555, 0.01846], ['gpt-35-turbo-16k', 350, 7.47555, 0.02136], ['gpt-35-turbo-16k', 177, 3.47804, 0.01965], ['gpt-35-turbo-16k', 236, 3.88216, 0.01645], ['gpt-4', 7, 1.83338, 0.26191], ['gpt-4', 22, 2.50587, 0.1139], ['gpt-4', 25, 2.50962, 0.10038], ['gpt-4', 66, 7.05846, 0.10695], ['gpt-4', 249, 38.3405, 0.15398], ['gpt-4', 106, 11.11538, 0.10486], ['gpt-4', 84, 9.6205, 0.11453], ['gpt-4', 376, 29.721, 0.07905], ['gpt-4', 136, 15.94493, 0.11724], ['gpt-4', 103, 10.54061, 0.10234], ['gpt-4-32k', 7, 2.47773, 0.35396], ['gpt-4-32k', 22, 3.10379, 0.14108], ['gpt-4-32k', 25, 2.18917, 0.08757], ['gpt-4-32k', 64, 5.89156, 0.09206], ['gpt-4-32k', 356, 40.15571, 0.1128], ['gpt-4-32k', 107, 10.26207, 0.09591], ['gpt-4-32k', 67, 12.07628, 0.18024], ['gpt-4-32k', 309, 42.49511, 0.13752], ['gpt-4-32k', 97, 7.57696, 0.07811], ['gpt-4-32k', 114, 7.98402, 0.07004], ['gcp-chat-bison-001', 7, 1.42634, 0.20376], ['gcp-chat-bison-001', 20, 1.32127, 0.06606], ['gcp-chat-bison-001', 12, 1.54062, 0.12838], ['gcp-chat-bison-001', 59, 1.64202, 0.02783], ['gcp-chat-bison-001', 87, 1.83678, 0.02111], ['gcp-chat-bison-001', 74, 1.83648, 0.02482], ['gcp-chat-bison-001', 56, 1.64675, 0.02941], ['gcp-chat-bison-001', 46, 1.48374, 0.03226], ['gcp-chat-bison-001', 28, 1.46616, 0.05236], ['gcp-chat-bison-001', 96, 2.16483, 0.02255], ['anthropic-claude-v2-100k', 7, 4.63135, 0.66162], ['anthropic-claude-v2-100k', 21, 2.91383, 0.13875], ['anthropic-claude-v2-100k', 47, 1.99142, 0.04237], ['anthropic-claude-v2-100k', 274, 11.10909, 0.04054], ['anthropic-claude-v2-100k', 357, 20.16475, 0.05648], ['anthropic-claude-v2-100k', 120, 5.00992, 0.04175], ['anthropic-claude-v2-100k', 172, 6.75014, 0.03925], ['anthropic-claude-v2-100k', 313, 12.97598, 0.04146], ['anthropic-claude-v2-100k', 281, 12.0365, 0.04283], ['anthropic-claude-v2-100k', 298, 18.70119, 0.06276], ['cohere-command', 131, 4.90621, 0.03745], ['cohere-command', 67, 2.76867, 0.04132], ['cohere-command', 99, 3.7577, 0.03796], ['cohere-command', 455, 14.43266, 0.03172], ['cohere-command', 499, 15.76886, 0.0316], ['cohere-command', 363, 11.47627, 0.03162], ['cohere-command', 243, 7.9184, 0.03259], ['cohere-command', 554, 17.44469, 0.03149], ['cohere-command', 448, 14.01322, 0.03128], ['cohere-command', 443, 13.93442, 0.03145], ['llama2-70b-chat-hf', 257, 11.3421, 0.04413], ['llama2-70b-chat-hf', 119, 6.22107, 0.05228], ['llama2-70b-chat-hf', 71, 3.49382, 0.04921], ['llama2-70b-chat-hf', 375, 15.05036, 0.04013], ['llama2-70b-chat-hf', 346, 15.4174, 0.04456], ['llama2-70b-chat-hf', 209, 9.03096, 0.04321], ['llama2-70b-chat-hf', 367, 15.4571, 0.04212], ['llama2-70b-chat-hf', 379, 15.45286, 0.04077], ['llama2-70b-chat-hf', 279, 12.03789, 0.04315], ['llama2-70b-chat-hf', 337, 14.0482, 0.04169], ['ai21-j2-jumbo-instruct', 7, 1.00308, 0.1433], ['ai21-j2-jumbo-instruct', 16, 1.14166, 0.07135], ['ai21-j2-jumbo-instruct', 16, 1.12577, 0.07036], ['ai21-j2-jumbo-instruct', 16, 1.42997, 0.08937], ['ai21-j2-jumbo-instruct', 16, 1.0194, 0.06371], ['ai21-j2-jumbo-instruct', 16, 1.22264, 0.07641], ['ai21-j2-jumbo-instruct', 16, 5.01028, 0.31314], ['ai21-j2-jumbo-instruct', 16, 0.96291, 0.06018], ['ai21-j2-jumbo-instruct', 16, 1.17927, 0.0737], ['ai21-j2-jumbo-instruct', 16, 1.02229, 0.06389], ['alephalpha', 7, 1.77926, 0.25418], ['alephalpha', 18, 3.43215, 0.19068], ['alephalpha', 26, 4.55511, 0.1752], ['alephalpha', 44, 7.31963, 0.16636], ['alephalpha', 95, 15.10179, 0.15897], ['alephalpha', 84, 13.53596, 0.16114], ['alephalpha', 60, 9.75345, 0.16256], ['alephalpha', 41, 6.88704, 0.16798], ['alephalpha', 200, 30.95972, 0.1548], ['alephalpha', 85, 13.45795, 0.15833]]

results = readFromFile("results.json") 

plt.figure(figsize=(10, 6))

for model in models:
    model_array = [result for result in results if result[0] == model]    
    model_array = sorted(model_array,key=lambda x: x[1])

    model_tokens = [arr[1] for arr in model_array]
    model_times = [arr[2] for arr in model_array]


    plt.plot(model_tokens, model_times, label=model)

plt.xlabel('Number of Tokens')
plt.ylabel('Time (s)')
plt.title('Latency of LLM Models')
plt.legend()
plt.tight_layout()
plt.show()