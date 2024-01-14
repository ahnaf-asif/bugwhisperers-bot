from helpers import get_today_timestamp, get_start_of_week_timestamp, get_start_of_month_timestamp
from api import get_user_submissions_by_count

class User:
    def __init__(self, username: str, name: str):
        self.username = username
        self.name = name
        self.daily_submissions = []
        self.weekly_submissions = []
        self.monthly_submissions = []

    async def filter_submissions(self, start_time, filter_type):
        
        submission_count = 50
        if filter_type == 'weekly':
            submission_count = 200
        elif filter_type == 'monthly':
            submission_count = 600
        
        try:
            submissions = await get_user_submissions_by_count(self.username, submission_count)
            unique_submissions = []

            for submission in submissions:
                if submission['verdict'] != 'OK':
                    continue
                if submission['creationTimeSeconds'] < start_time:
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

                if entry not in unique_submissions:
                    unique_submissions.append(entry)
            return unique_submissions
        except Exception as e:
            print(f'Error in models/user.py: {e}')
            return e

    async def get_daily_submissions(self):
        today = get_today_timestamp()
        
        try:
            return await self.filter_submissions(today, 'daily')
        except Exception as e:
            print(f'Error in models/user.py: {e}')
            return e

    async def get_weekly_submissions(self):
        this_week = get_start_of_week_timestamp()
        
        try:
            return await self.filter_submissions(this_week, 'weekly')
        except Exception as e:
            print(f'Error in models/user.py: {e}')
            return e

    async def get_monthly_submissions(self):
        this_month = get_start_of_month_timestamp()
        
        try:
            return await self.filter_submissions(this_month, 'monthly')
        except Exception as e:
            print(f'Error in models/user.py: {e}')
            return e

    async def get_summary(self):
        self.daily_submissions = await self.get_daily_submissions()
        self.weekly_submissions = await self.get_weekly_submissions()
        self.monthly_submissions = await self.get_monthly_submissions()

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
