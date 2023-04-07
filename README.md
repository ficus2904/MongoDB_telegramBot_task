# MongoDB Data Query with AIogram Bot

This Python code queries MongoDB and generates an output based on input date range and group type, powered by the AIogram Bot framework.

## Installation

Create a virtual environment and install the dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Configuration

You need to have a MongoDB instance running with a valid URI. Once that is done, replace the 'mongodb://localhost:27017/' string in line 9 with your URI.

Also, you need to create a `key.txt` file containing the API token of your Telegram bot.

## Functionality

This code exposes a message handler function that allows the user to query MongoDB via a Telegram bot. The message content should be in JSON format with three fields: `dt_from`, `dt_upto`, and `group_type`.

The `dt_from` and `dt_upto` parameters represent the date range of the query, and the `group_type` parameter represents the group type that will be generated in the output.

The `alter_input` function converts the input date string to a valid datetime format for the MongoDB query.

The `add_null_steps` function ensures that missing time steps (if any) are included in the output by adding a `0` value to the dataset for those dates.

The `query_mongodb` function queries the MongoDB instance with the input data and applies the `add_null_steps` function to the output to generate the final result.

Once the query is completed, the bot sends the output to the user.

## Usage

To use the bot, send a message to it with the following format:

```
{"dt_from": "<date_from>", "dt_upto": \"<date_upto>", "group_type": "<group_type>"}
```

Where `<date_from>` is the lower range of the query (in "YYYY-MM-DDTHH:mm:ss" format), `<date_upto>` is the upper range of the query (in "YYYY-MM-DDTHH:mm:ss" format), and `<group_type>` is the time unit to group the output (either "year", "month", "day", or "hour").

## Example

```
{"dt_from": "2022-01-01T00:00:00", "dt_upto": "2022-02-01T00:00:00", "group_type": "day"}
```

This query will generate a dataset with hourly time steps between January 1st and February 1st, 2022, and group them by day.

## Demo
https://t.me/taskJsonMongoBot