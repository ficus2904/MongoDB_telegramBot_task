import pymongo
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from aiogram import Bot, Dispatcher, types, executor
import json

# Initializing MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Function to alter input data format
def alter_input(input_data):
    if len(input_data) == 19:
        return datetime.fromisoformat(input_data)
    return {'year': "%Y-01-01T00:00:00",
            'month':"%Y-%m-01T00:00:00",
            'day':"%Y-%m-%dT00:00:00",
            'hour':"%Y-%m-%dT%H:00:00"}.get(input_data)

# Function to generate missing steps in the dataframe
def add_null_steps(df,input_data):
    start_date = alter_input(input_data['dt_from'])
    end_date = alter_input(input_data['dt_upto'])
    step = relativedelta(**{f"{input_data['group_type']}s":1})

    current_date = start_date
    date_list = []

    while current_date <= end_date:
        date_string = current_date.strftime('%Y-%m-%dT%H:00:00')
        date_list.append(date_string)
        current_date += step

    dates_null = list(set(date_list).difference(set(df.labels)))
    new_df = pd.DataFrame({'dataset': [0]*len(dates_null), 'labels': dates_null})
    new_df = pd.concat([df, new_df], axis=0).sort_values(by='labels').reset_index(drop=True)
    new_df.dataset = new_df.dataset.astype(int)
    return new_df.to_dict('list')

# Function to query MongoDB and generate the output
async def query_mongodb(input_data):
    pipeline = [
        {"$match": {"dt": {"$gte": alter_input(input_data['dt_from']), "$lte": alter_input(input_data['dt_upto'])}}},
        {"$group": {"_id": {"$dateToString": {"format": alter_input(input_data['group_type']), "date": "$dt"}}, "total_salary": {"$sum": "$value"}}},
        {"$sort": {"_id": 1}},
        {"$group": {"_id": None, "dataset": {"$push": "$total_salary"}, "labels": {"$push": "$_id"}}},
        {"$project": {"_id": 0, "dataset": 1, "labels": 1}}
    ]

    result = list(collection.aggregate(pipeline))[0]
    output = add_null_steps(pd.DataFrame(result),input_data)

    return output

# Creating the bot and defining the handler
with open("key.txt", "r") as file:
    key = file.read()
    
bot = Bot(token=key)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    input_data = json.loads(message.text)

    if len(input_data) != 3:
        await message.reply("Invalid input format. Please enter date_from, date_upto and group_type separated by space.")
        return

    try:
        output = await query_mongodb(input_data)
        await message.reply(output)
    except Exception as e:
        await message.reply(f"Error occurred while querying database: {str(e)}")
        return

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
