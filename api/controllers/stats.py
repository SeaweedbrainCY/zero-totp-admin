from flask import request, Response, redirect, make_response
from database.repositories import user as user_repo
import datetime as dt



def get_users_per_category():
    users = user_repo.get_all_users()
    total_users = len(users)
    verified_users = len([user for user in users if user.isVerified])
    blocked_users = len([user for user in users if user.isBlocked])
    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "blocked_users": blocked_users,
    }

def get_user_timechart():
    first_date_to_count = (dt.datetime.now() - dt.timedelta(days=365)).replace(day=1)
    # For each month detected in the db, we count the number of new users
    users = user_repo.get_all_users()
    new_users_per_months = {}
    for user in users:
        creation_date = dt.datetime.strptime(user.createdAt, "%d/%m/%Y").replace(day=1)
        if creation_date >= first_date_to_count:
            new_users_per_months[creation_date.strftime("%Y-%m-%d")] = new_users_per_months.get(creation_date.strftime("%Y-%m-%d"), 0) + 1
        else:
            new_users_per_months[first_date_to_count.strftime("%Y-%m-%d")] = new_users_per_months.get(first_date_to_count.strftime("%Y-%m-%d"), 0) + 1
    total_users_per_months = {first_date_to_count.strftime("%Y-%m-%d") : 0}
    # instantiate a dict with all months from the first month to count to now
    previous_month = first_date_to_count
    previously_counted_users = 0
    for _ in range(1, 12):
        next_month = (previous_month + dt.timedelta(days=40)).replace(day=1)# + 40d to be sure to be in the next month
        previously_counted_users += new_users_per_months.get(next_month.strftime("%Y-%m-%d"), 0)
        total_users_per_months[next_month.strftime("%Y-%m-%d")] = previously_counted_users

        previous_month = next_month
    
    
    return total_users_per_months


    