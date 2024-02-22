from transformers import LlamaForCausalLM, LlamaTokenizer

hf_access_token = "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"

tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=hf_access_token)
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", load_in_8bit=True, device_map="auto", token=hf_access_token)


import json
with open("json_edge_data_list_elon.json", "r") as out:
    ne = json.load(out)
    
with open("json_node_data_list_elon.json", "r") as out:
    node_data = json.load(out)
    
with open("json_replies_data_list_elon.json", "r") as out:
    replies_data = json.load(out)
    
import networkx as nx

        
from bs4 import BeautifulSoup
def process_text(text):
    fc=""
    soup = BeautifulSoup(text,'html.parser')
    ptags = soup.find_all('p')
    for p_tag in ptags:
        fc += p_tag.get_text()
    return fc

def llama2_system_talk(system, text):
    gen_len = 50

    generation_kwargs = {
          "max_new_tokens": gen_len,
          "top_p": 0.9,
          "temperature": 0.5,
          "repetition_penalty": 1.2,
          "do_sample": True,
      }

    B_INST, E_INST = "[INST]", "[/INST]"

    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    system_prompt = system

    prompt_text = text

    prompt = f"{B_INST} {B_SYS} {system_prompt} {E_SYS} {prompt_text} {E_INST}"  # Special format required by the Llama2 Chat Model where we can use system messages to provide more context about the task

    prompt_ids = tokenizer(prompt, return_tensors="pt")

    prompt_size = prompt_ids['input_ids'].size()[1]

    generate_ids = model.generate(prompt_ids.input_ids.to(model.device), **generation_kwargs)

    generate_ids = generate_ids.squeeze()

    response = tokenizer.decode(generate_ids.squeeze()[prompt_size+1:], skip_special_tokens=True).strip()

    return response

def classify(input_text):
        system_prompt = "Classify the given tweet in one of the three categories: pro-elon, neutral, anti-elon and give output as 1 for pro-elon, 0 for neutral and -1 for anti-elon. For tweets containting ';;', consider the second part for the classification and first part as the context. Do not give any explaination or justification. Just give the rating value as the output and do not give any other text. "

    return llama2_system_talk(system_prompt, input_text)


def main():
    G = nx.DiGraph()
    for x in ne.keys():
        for y in ne[x]:
            G.add_edges_from([(y,x)])

    node_text_data = {}
    for nodes in G.nodes:
        flag = False
        for y in node_data.keys():
            if(str(nodes)==str(node_data[y]['acc_id'])):
                text = node_data[y]['content']
                text = process_text(text)
    #             print(text)
                flag = True
                break
        if(flag==False):
            for y in replies_data.keys():
                if(str(nodes)==str(replies_data[y]['acc_id'])):

                    text = replies_data[y]['content']
                    text1 = process_text(text.split(';;')[0])
                    text2 = process_text(text.split(';;')[1])
                    text =  text1+ ';;'+text2
    #                 print(text)
                    flag = True
    #                 break
    #     print(flag)
        node_text_data[str(nodes)] = text
    #     break

    node_labels = {}
    node_list = list(G.nodes)
    for i in range(len(node_list[50:100])):

        text = node_text_data[str(node_list[i])]
        res = str(classify(text))
        if("-1" in res):
            node_labels[node_list[i]] = "red"
        elif("1" in res):
            node_labels[node_list[i]] = "green"
        else:
            node_labels[node_list[i]] = "blue"
        print(i,node_labels[node_list[i]])
    #     
    #     print(res)

    node_labels = json.dumps(node_labels, indent=4)
    with open("node_labels.json", "w") as outfile:
        outfile.write(node_labels)
    
if __name__ == '__main__':
    main()

