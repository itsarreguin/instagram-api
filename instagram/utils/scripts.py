import csv

# Instagram models
from instagram.core.models import User


UPPPER_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LOWER_CHARS = 'abcdefghijklmnopqrstuvwxyz'

SPECIAL_CHARS = '_-'

NUMBER_CHARS = '0123456789'

RAND_CHARS = UPPPER_CHARS + LOWER_CHARS + SPECIAL_CHARS + NUMBER_CHARS


def users_loader(filename: str = None):
    """
    Users loader read a csv file to generate users and their profiles.

    Args:
        filename (str, required): Allows a csv file.
    """
    with open(file=filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            User.objects.bulk_create(
                User(
                    first_name=row[0],
                    last_name=row[1],
                    username=row[2],
                    email=row[3],
                    password=row[4],
                    is_verified=row[5] == '1'
                )
            )