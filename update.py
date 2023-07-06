import requests
import json
from pprint import pprint
import sqlite3
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.twitch.tv/helix/users'

headers = {
    'client-id' : os.getenv("twitch_client_id"),
    'Authorization' : os.getenv("twitch_app_access_token")
}



while True:
    try:
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute("SELECT id FROM member_data")

        rows = cur.fetchall()

        for row in rows:
            params = {'id': row[0]}
            response = requests.get(url, headers=headers, params=params)
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

    time.sleep(86400)

