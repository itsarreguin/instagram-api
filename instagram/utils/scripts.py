import csv

# Instagram models
from instagram.core.models import User


def users_loader(filename: str = None):
    """users loader

    Args:
        filename (str, required):
            Allows a csv file to read data and generate users in the db.
    """
    with open(file=filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            User.objects.create_user(
                first_name=row[0],
                last_name=row[1],
                username=row[2],
                email=row[3],
                password=row[4],
                is_verified=row[5] == '1'
            )