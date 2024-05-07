import requests, time, os, json
from transformers import AutoTokenizer
from transformers import GPT2TokenizerFast

token = None
URL = os.getenv("LLM_API_BASE")

model_cases = {
    "gpt": lambda q, model: {
        "data": {"deployment_id": model, "messages": [{"role": "user", "content": q}], "max_tokens": 400},
        "process": lambda response, t: [model, response.json()["usage"]["completion_tokens"], t],
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['choices'][0]['message']['content']} Time (in s): {t}")
    },
    "cohere-command": lambda q, model: {
        "data": {"deployment_id": model, "prompt": q, "max_tokens": 400},
        "process": lambda response, t: [model, response.json()["meta"]["billed_units"]["output_tokens"], t],
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['generations'][0]['text']} Time (in s): {t}")
    },
    "ai21-j2-jumbo-instruct": lambda q, model: {
        "data": {"deployment_id": model, "prompt": q, "maxTokens": 400},
        "process": lambda response, t: [model, len(response.json()["completions"][0]["data"]["tokens"]), t],
        "print": lambda response, t: print(f"{model} Answer: {response.json()['completions'][0]['data']['text']} Time (in s): {t}")
    },
    "alephalpha": lambda q, model: {
        "data": {"deployment_id": model, "prompt": q, "maximum_tokens": 400},
        "process": lambda response, t: [model, response.json()["num_tokens_generated"], t],
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['completions'][0]['completion']} Time (in s): {t}")
    },
    "gcp-chat-bison-001": lambda q, model: {
        "data": {"deployment_id": model, "instances": [{"messages": [{"author": "user", "content": q}]}], "parameters": {"maxOutputTokens": 400}},
        "process": lambda response, t: [model, response.json()["metadata"]["tokenMetadata"]["outputTokenCount"]["totalTokens"], t],
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['predictions'][0]['candidates'][0]['content']} Time (in s): {t}")
    },
    "llama2-70b-chat-hf": lambda q, model: {
        "data": {"deployment_id": model, "inputs": q, "parameters": {"max_new_tokens": 400}},
        "process": lambda response, t: [model, len(llama2Tokenizer.tokenize(response.json()["generated_text"])), t], 
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['generated_text']} Time (in s): {t}")
    },
    "anthropic-claude-v2-100k": lambda q, model: {
        "data": {"deployment_id": model, "prompt": f"\n\nHuman:{q}\n\nAssistant:", "max_tokens_to_sample": 400},
        "process": lambda response, t: [model, len(claude2Tokenizer.tokenize(response.json()["completion"])), t],
        "print": lambda response, t: print(f"{model}: Answer: {response.json()['completion']} Time (in s): {t}")
    }
}

def get_token():
    global token
    if token is None:
        client_id = os.getenv("LLM_CLIENT_ID")
        client_secret = os.getenv("LLM_CLIENT_SECRET")

        params = {"grant_type": "client_credentials" }
        resp = requests.post(f"{os.getenv('LLM_AUTH_URL')}/oauth/token",
                            auth=(client_id, client_secret),
                            params=params)

        token = resp.json()["access_token"]

    return token

def make_request(data):
    my_token = get_token()

    headers = {
        "Authorization":  f"Bearer {my_token}",
        "Content-Type": "application/json"
    }

    start = time.time()
    try:
        response = requests.post(URL + '/api/v1/completions',
                            headers=headers,
                            json=data)
    except Exception as err:
        print(err)
    
    end = time.time() - start

    return response, end

def writeToFile(results):
    filename = "results.json"

    try:
        with open(filename, "x") as file:
            json.dump(results, file)

    except FileExistsError:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        with open(new_filename, "x") as file:
            json.dump(results, file)
            print(f"The file '{new_filename}' was created successfully.")
    else:
        print(f"The file '{filename}' was created successfully.")

def run(model):
    for q in questions:
        if "gpt" in model: case = model_cases.get("gpt")
        else: case = model_cases.get(model)

        case_data = case(q, model)

        response, t = make_request(case_data["data"])

        if response.status_code == 200:
            results.append(case_data["process"](response, t))
            case_data["print"](response, t)
        else:
            print(f"Error occurred!\n{response.json()}")


if __name__ == "__main__":
    
    llama2Tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-70b-chat-hf')
    claude2Tokenizer = GPT2TokenizerFast.from_pretrained('Xenova/claude-tokenizer')
    # auth on cli: huggingface-cli login

    results = list()

    models= ["gpt-35-turbo-16k", "gpt-4","gpt-4-32k","gpt-4-turbo","gcp-chat-bison-001","anthropic-claude-v2-100k","cohere-command","llama2-70b-chat-hf","ai21-j2-jumbo-instruct","alephalpha"]

    questions = ["What is the capital of Australia?","What is the distance between the Earth and the Moon?","Who was the first woman to win a Nobel Prize?","What is the law of conservation of energy?","How does a combustion engine work?","What is the Pythagorean theorem?","What is a utility analysis?","What are the key principles of quantum mechanics?","What is the BLEU score in Machine Learning?","What is the F-1 score in Machine Learning?"]
    
    for i in range(1,11):
        print(f"Run {i} started!")
        for model in models:
            run(model)
            
    res = [sublist + [round(sublist[2]/sublist[1],5)] for sublist in results]

    writeToFile(res)