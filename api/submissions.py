import aiohttp
import json

async def get_user_submissions_by_count(username, count):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://codeforces.com/api/user.status?handle={username}&from=1&count={count}") as resp:
                data = await resp.json()
                submissions = data['result']
                return submissions
    except Exception as e:
        print(f'Error in api/submissions.py: {e}')
        return e