import requests
import json
from pprint import pprint
import sqlite3
import time
from datetime import datetime
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token")
}


async def image_url_update():
    while True:
        try:
            conn = sqlite3.connect("data.db")
            cur = conn.cursor()

            cur.execute("SELECT id FROM member_data")

            rows = cur.fetchall()

            for row in rows:
                params = {'id': row[0]}
                response = requests.get('https://api.twitch.tv/helix/users', headers=headers, params=params)
                contents = json.loads(response.content)

                profile = contents['data'][0]['profile_image_url'].split('/')[-1].split('-profile')[0]
                offline = contents['data'][0]['offline_image_url'].split('/')[-1].split('-channel')[0]

                cur.execute(f"UPDATE member_data SET profile = '{profile}' WHERE id = {row[0]}")
                conn.commit()
                cur.execute(f"UPDATE member_data SET offline = '{offline}' WHERE id = {row[0]}")
                conn.commit()

            conn.close()

            print(datetime.now())

        except:
            conn.close()
            pass

        await asyncio.sleep(86400)

async def live_update():
    while True:
        try:
            conn = sqlite3.connect("data.db")
            cur = conn.cursor()

            cur.execute("SELECT id FROM member_data")

            rows = cur.fetchall()

            for row in rows:
                params = {'user_id': row[0]}
                response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=params)
                contents = json.loads(response.content)
                try:
                    if contents["data"][0]["type"] == 'live':
                        cur.execute(f"UPDATE member_data SET live = 1 WHERE id = {row[0]}")
                except:
                    cur.execute(f"UPDATE member_data SET live = 0 WHERE id = {row[0]}")
                conn.commit()

            conn.close()

            print(datetime.now())
        
        except:
            conn.close()
            pass

        await asyncio.sleep(300)


async def main():
    image_url = asyncio.create_task(image_url_update())
    live = asyncio.create_task(live_update())

    await image_url
    await live


if __name__ == "__main__":
    asyncio.run(main())





# while True:
#     try:
#         conn = sqlite3.connect("data.db")
#         cur = conn.cursor()

#         cur.execute("SELECT id FROM member_data")

#         rows = cur.fetchall()

#         for row in rows:
#             params = {'id': row[0]}
#             response = requests.get(user_url, headers=headers, params=params)
#             contents = json.loads(response.content)

#             profile = contents['data'][0]['profile_image_url'].split('/')[-1].split('-profile')[0]
#             offline = contents['data'][0]['offline_image_url'].split('/')[-1].split('-channel')[0]

#             cur.execute(f"UPDATE member_data SET profile = '{profile}' WHERE id = {row[0]}")
#             conn.commit()
#             cur.execute(f"UPDATE member_data SET offline = '{offline}' WHERE id = {row[0]}")
#             conn.commit()

#         conn.close()

#         print(datetime.now())

#     except:
#         conn.close()
#         pass

#     time.sleep(86400)

