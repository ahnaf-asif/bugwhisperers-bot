from helpers import get_today_timestamp, get_start_of_week_timestamp, get_start_of_month_timestamp
from api import get_user_submissions_by_count

class User:
    def __init__(self, username: str, name: str):
        self.username = username
        self.name = name
        self.daily_submissions = []
        self.weekly_submissions = []
        self.monthly_submissions = []

    async def set_submissions(self):
        today = get_today_timestamp()
        this_week = get_start_of_week_timestamp()
        this_month = get_start_of_month_timestamp()

        try:
            submissions = await get_user_submissions_by_count(self.username, 400)

            for submission in submissions:
                if submission['verdict'] != 'OK':
                    continue
                if submission['creationTimeSeconds'] < this_month:
                    break

                problem = submission['problem']
                rating = None

                if 'rating' not in problem:
                    rating = 1000
                else:
                    rating = problem['rating']

                entry = {
                    'problem': problem['name'],
                    'problem_index': problem['index'],
                    'contest': problem['contestId'],
                    'timestamp': submission['creationTimeSeconds'],
                    'rating': rating
                }

                if entry not in self.daily_submissions and entry['timestamp'] >= today:
                    self.daily_submissions.append(entry)
                if entry not in self.weekly_submissions and entry['timestamp'] >= this_week:
                    self.weekly_submissions.append(entry)
                if entry not in self.monthly_submissions and entry['timestamp'] >= this_month:
                    self.monthly_submissions.append(entry)
            
        except Exception as e:
            print(f'Error in models/user.py/set_submissions: {e}')

    async def get_summary(self):
        try:
            await self.set_submissions()

            daily_score = 0
            weekly_score = 0
            monthly_score = 0

            for submission in self.daily_submissions:
                daily_score += ((submission['rating'] / 100)**5)/(10**4)
            for submission in self.weekly_submissions:
                weekly_score += ((submission['rating'] / 100)**5)/(10**4)
            for submission in self.monthly_submissions:
                monthly_score += ((submission['rating'] / 100)**5)/(10**4)
            
            return {
                'name': self.name,
                'daily_score': round(daily_score, 2),
                'weekly_score': round(weekly_score, 2),
                'monthly_score': round(monthly_score, 2)
            }
        except Exception as e:
            print(f'Error in models/user.py/get_summary: {e}')
            return e
