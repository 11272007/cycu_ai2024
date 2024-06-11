import requests

rd = requests.post(
    f"https://notify-api.line.me/api/notify",
    headers={"Authorization": f"Bearer {'y5URlJSrxYiyae1r09V6DMV8xEEzie59hKzlfr6CJjj'}"},
    data={"message": f"{'蕭銘斈'}"})