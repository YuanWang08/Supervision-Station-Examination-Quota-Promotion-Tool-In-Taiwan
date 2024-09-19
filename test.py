from crud.get_and_delete_shortDb import get_and_delete_shortDb
from main.sendNotify import sendNotify


data = get_and_delete_shortDb()
sendNotify(data)