from flask import request, Response, redirect, make_response
from database.repositories import user as user_repo
import datetime as dt



def get_users_stats():
    users = user_repo.get_all_users()
    total_users = len(users)
    verified_users = len([user for user in users if user.isVerified])
    blocked_users = len([user for user in users if user.isBlocked])
    first_date_to_count = (dt.datetime.now() - dt.timedelta(days=365))
    new_users_per_months = {}
    # For each month detected in the db, we count the number of new users
    for user in users:
        creation_date = dt.datetime.strptime(user.createdAt, "%d/%m/%Y")
        if creation_date < first_date_to_count:
            creation_month = first_date_to_count.strftime("%B %Y")
        else:
            creation_month = creation_date.strftime("%B %Y")
        if creation_month not in new_users_per_months:
            new_users_per_months[creation_month] = 0
        new_users_per_months[creation_month] += 1
    months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    total_user_per_months = {} # final result
    first_mount_i = months_list.index(first_date_to_count.strftime("%B"))
    new_users_months = new_users_per_months.keys()
    # the goal is, for each month, starting with the first month of count (month 1 year ago), to sum the number of new users for each month with the previous month
    if first_date_to_count.strftime("%B") in new_users_months:
        total_user_per_months[first_date_to_count.strftime("%B %Y")] = new_users_per_months[first_date_to_count.strftime("%B %Y")]
    else:
        total_user_per_months[first_date_to_count.strftime("%B %Y")] = 0
    for i in range(1,13):
        current_year = first_date_to_count.year if first_date_to_count.month + i <= 12 else first_date_to_count.year + 1
        previous_month_year = first_date_to_count.year if first_date_to_count.month + i - 1 <= 12 else first_date_to_count.year + 1 # if we are in january, we need to go back to the previous year
        month = months_list[(first_mount_i + i) % 12] + " " + str(current_year)
        if month in new_users_months:
            total_user_per_months[month] = new_users_per_months[month] + total_user_per_months[months_list[(first_mount_i + i - 1) % 12] + " " + str(previous_month_year)]
        else:
            total_user_per_months[month] = total_user_per_months[months_list[(first_mount_i + i - 1) % 12] + " " + str(previous_month_year)]


    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "blocked_users": blocked_users,
        "total_user_per_month_over_year": total_user_per_months
    }