import os
from datetime import datetime
from shutil import rmtree


path_to_data = '/home/teamlary/mintsData/reference/001e0610c2e7'

current_date = str(datetime.date(datetime.now())).split('-')
year = current_date[0]
month = int(current_date[1])

if month == 1:
    month_to_remove = 11
elif month == 2:
    month_to_remove = 12
else:
    month_to_remove = month - 2


month_to_remove = str(month_to_remove).zfill(2)

path_to_remove = os.path.join(path_to_data, year, month_to_remove )

if os.path.exists(path_to_remove):
    print("Removing {}".format(path_to_remove))
    rmtree(path_to_remove)
