from typing import Final
import aiohttp
import json
from helper import get_today_timestamp, get_start_of_week_timestamp, get_start_of_month_timestamp

async def get_summary():
    USERS: Final = [
        {'username': 'Ahnaf.Shahriar.Asif', 'name': 'Ahnaf Shahriar Asif'},
        {'username': 'mub.ch', 'name': 'Mubasshir Chowdhury'},
        {'username': '_blaNk_', 'name': 'Shafin Alam'}
    ]

    today = get_today_timestamp()
    start_of_week = get_start_of_week_timestamp()
    start_of_month = get_start_of_month_timestamp()

    result = []

    print(USERS)

    try:    
        for user in USERS:
            print(f"current user: {user['name']}")
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://codeforces.com/api/user.status?handle={user['username']}&from=1&count=400") as resp:
                    data = await resp.json()
                    submissions = data['result']

                    unique_daily_submissions = []
                    unique_weekly_submissions = []
                    unique_monthly_submissions = []

                    for submission in submissions:
                        if submission['verdict'] != 'OK':
                            continue
                        if submission['creationTimeSeconds'] < start_of_month:
                            break

                        problem = submission['problem']

                        entry = {
                            'problem': problem['name'],
                            'contest': problem['contestId'],
                            'timestamp': submission['creationTimeSeconds'],
                            'rating': problem['rating']
                        }

                        if submission['creationTimeSeconds'] >= today and entry not in unique_daily_submissions:
                            unique_daily_submissions.append(entry)
                        if submission['creationTimeSeconds'] >= start_of_week and entry not in unique_weekly_submissions:
                            unique_weekly_submissions.append(entry)
                        if entry not in unique_monthly_submissions:
                            unique_monthly_submissions.append(entry)

                    daily_score = 0
                    weekly_score = 0
                    monthly_score = 0

                    for submission in unique_daily_submissions:
                        print('here is a submission: ', submission)
                        daily_score += ((submission['rating'] / 100)**5)/(10**4)
                    for submission in unique_weekly_submissions:
                        weekly_score += ((submission['rating'] / 100)**5)/(10**4)
                    for submission in unique_monthly_submissions:
                        monthly_score += ((submission['rating'] / 100)**5)/(10**4)
                    result.append({
                        'name': user['name'],
                        'daily_score': round(daily_score, 2),
                        'weekly_score': round(weekly_score, 2),
                        'monthly_score': round(monthly_score, 2)
                    })
        result.sort(key=lambda x: x['monthly_score'], reverse=True)
        return result
    except Exception as e:
        print(e)
        return e