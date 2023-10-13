import openai
import pandas as pd
import io

df = pd.read_csv(r"C:\Users\wccha\Documents\Rutgers\Topics in AI\hippocorpus\hcV3-stories.csv")

openai.api_key = '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'

system_prompt = "Given a short prompt summary, write an imagined journal or diary entry about an event. After writing, answer a few questions. The story must correspond to the summary. Pretend the event happened to you, but do not write about something that actually happened to you. Write using first person perspective. Use the timeline of when the event happened. Story must be 1 sentences and 6-30 characters including spaces. Do not use salutations such as 'Dear Diary' or 'Dear Journal' or 'Journal Entry' or stating the date the event happened."
prompt_start = "Summary:"
prompt_middle = "- happened: "
prompt_end = " days ago"
Chat_GPT_Imagined_Stories = []
finished_summary_ids = []
counter = 0
total_time = 0
total_counter = 0
test_counter = 0

for i in range(len(df['summary'])):
  id_summary = []
  if df['recImgPairId'][i] and pd.notnull(df['recImgPairId'][i]):
    id_summary.append(df['recImgPairId'][i])
  elif df['recAgnPairId'][i] and pd.notnull(df['recAgnPairId'][i]):
    df['recImgPairId'][i] = df['recAgnPairId'][i]
    id_summary.append(df['recAgnPairId'][i])
  else:
    id_summary.append('NAPairId')
  if id_summary[0] not in finished_summary_ids:
    prompt = prompt_start + df['summary'][i] + prompt_middle + str(df['logTimeSinceEvent']) + prompt_end
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    id_summary.append(completion.choices[0].message.content)
    Chat_GPT_Imagined_Stories.append(id_summary)
    finished_summary_ids.append(id_summary[0])

    total_counter = total_counter + 1
    test_counter = test_counter + 1
    
    print(total_counter)
    
  # if test_counter >= 2:
  #   break
for i in Chat_GPT_Imagined_Stories:
  print(i)
  
GPT_Stories_df = pd.DataFrame(Chat_GPT_Imagined_Stories)
GPT_Stories_df.rename(columns={0: "recImgPairId"}, inplace=True)
GPT_Stories_df.rename(columns={1: "GPT_Story"}, inplace=True)
merged_df = pd.merge(df, GPT_Stories_df, on = "recImgPairId", how = "left")

GPT_Stories_df.to_csv("C:\Users\wccha\Documents\Rutgers\Topics in AI\GPT_Stories_df.csv")
merged_df.to_csv("C:\Users\wccha\Documents\Rutgers\Topics in AI\merged_df.csv")