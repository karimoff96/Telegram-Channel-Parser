from pyrogram import Client, filters
from datetime import datetime
import mysql.connector

# getting personal IDs from https://my.telegram.org/auth and creating bot client which works as telegram userbot.
bot = Client(
    session_name="session_name",  # session_name
    api_id='api_id',  # api_id
    api_hash='api_hash',  # api_hash
)
x = input('Enter the keyword: ')  # userbot will search and get data from channels by the inputted keyword


@bot.on_message(filters.channel & filters.regex(
    f"{x}"))  # filtering type of objects for search, we specified it as 'channel' so the userbot will look up channels for given keyword
def catcher_msg(client, message):
    # all found messages with keyword would be formatted as dictionary called "json_data"
    json_data = {
        'Type': message.chat.type,
        'Name': message.chat.title,
        'Username': message.chat.username,
        'Text': message.text,
        'Views': message.views,
        'Author': message.author_signature,
        'Date': datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
        # this is needed for formatting "Unix datetime" into "Local datetime"
    }
    print(json_data)

    # connecting mysql database with app
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",  # username
        password="pasword",  # pasword
        database="database_name"  # database name
    )

    mycursor = mydb.cursor()
    # storing json data for more accurate database format
    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in json_data.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in json_data.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('database_table_name', columns, values)
    mycursor.execute(sql,
                     json_data)  # inserting our json_data into database called json and storing it in 'MESSAGES' table
    mydb.commit()
    print(sql)


print(f'form now the app will parse telegram channels by the "{x}" keyword')
bot.run()
