import aiohttp
import json

async def get_user_submissions_by_count(username, count):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://codeforces.com/api/user.status?handle={username}&from=1&count={count}") as resp:
                if resp.content_type == 'application/json':
                    data = await resp.json()
                    if 'result' in data:
                        submissions = data['result']
                        return submissions
                    else:
                        print(f'Error in api/submissions.py: Unexpected JSON format - missing "result" key')
                        return None
                else:
                    print(f'Error in api/submissions.py: Unexpected content type - {resp.content_type}', resp)
                    return None
    except Exception as e:
        print(f'Error in api/submissions.py: {e}')
        return e