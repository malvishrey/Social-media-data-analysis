import json
import requests
import pandas as pd
from mastodon import Mastodon

temp = Mastodon(client_id='PIKL3IEgYnqfXmPvQs4v4UC0GkKgyuPGY7VkYQlBNdY', 
                client_secret='6ObxNMAgQUmReBybEx42IWH_G6kDtzvqIX_VsiRoHcE', 
                access_token='NFfo0Zjz2FSMT4L2w-X_1HiOYNQ7eLXIbQggovjgwl4',
                api_base_url='https://mastodon.social')

hashtags = ['elon','elonmusk','twitter']

def get_data(hashtags,limit=40):
    results = []

    for h in hashtags:
        max_id = None
        c = 0
        while(c<limit):
            X = temp.timeline_hashtag(h,limit=40,max_id = max_id)
            toots = X
            print(len(toots))

            if len(toots) == 0:
                break

            for t in toots:
                if(t['in_reply_to_id'] is None):
                    results.append(t)

            max_id = toots[-1]['id']
            print(max_id)
            c += 1

    df = pd.DataFrame(results)
    return df


unique_nodes = []
network_edges = []
node_data_list = {}
replies_data_list = {}

def create_json(df):
    c = 0
    dc = 0
    for i in range(len(df)):
        # print(i)
        # if(df.iloc[i]['account']['id'] not in unique_nodes):
        c += 1
        #     unique_nodes.append(df.iloc[i]['account']['id'])
        node_data = {}
        node_data['acc_id'] = df.iloc[i]['account']['id']
        node_data['content'] = df.iloc[i]['content']
        node_data['tags'] = df.iloc[i]['tags']

        node_data_list[df.iloc[i]['id']] = node_data

        desc = temp.status_context(df.iloc[i]['id'])['descendants']
        # replies = []
        if(len(desc)>3 and len(desc)<8):
            dc += 1
            print('reach')
            for d in desc:
                if(d['account']['id'] != df.iloc[i]['account']['id']):

                    replies_data = {}
                    replies_data['parent_id'] = df.iloc[i]['account']['id']
                    replies_data['acc_id'] = d['account']['id']
                    replies_data['content'] = df.iloc[i]['content'] + ';;' + d['content']
                    replies_data['tags'] = df.iloc[i]['tags'] + d['tags']
                    replies_data_list[d['id']] = replies_data

                    network_edges.append([df.iloc[i]['account']['id'],d['account']['id']])
            # # print(df.iloc[i]['account']['id'])
            print(c,dc)       

            
def save_data():
    for x in node_data_list.keys():
        node_data_list[x]['acc_id'] = str(node_data_list[x]['acc_id'])
        # break
    new_node_data_list = {}
    for x in node_data_list.keys():
        new_node_data_list[str(x)] = node_data_list[x]
        
    for x in replies_data_list.keys():
        replies_data_list[x]['parent_id'] = str(replies_data_list[x]['parent_id'])
        replies_data_list[x]['acc_id'] = str(replies_data_list[x]['acc_id'])
        # break
    new_replies_data_list = {}
    for x in replies_data_list.keys():
        new_replies_data_list[str(x)] = replies_data_list[x]
        
        
    edge_data = {}
    for x,y in network_edges:
        if x in edge_data.keys():
            edge_data[x].append(str(y))
        else:
            edge_data[x] = [str(y)]
    
    json_node_data_list = json.dumps(new_node_data_list, indent=4)
    with open("json_node_data_list_elon.json", "w") as outfile:
        outfile.write(json_node_data_list)

    json_replies_data_list = json.dumps(new_replies_data_list, indent=4)
    with open("json_replies_data_list_elon.json", "w") as outfile:
        outfile.write(json_replies_data_list)
        
    json_edge_data_list = json.dumps(edge_data, indent=4)
    with open("json_edge_data_list_elon.json", "w") as outfile:
        outfile.write(json_edge_data_list)
        
            
df = get_data(hashtags)
create_json(df)
save_data()

