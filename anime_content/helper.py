import datetime
import random
import string


def generate_unique_filename(extension):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"{current_datetime}_{random_suffix}.{extension}"