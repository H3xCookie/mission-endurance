import datetime
from subprocess import run


def send_message_down(message: str):
    time = datetime.datetime.now()
    time_date, time_time = str(time).split(" ")
    time = f"{time_date}T{time_time}"
    time = time.replace(":", "_")
    time = time.replace(".", "_")
    filename = f"./transfer_file_{time}.txt"
    with open(filename, "w") as file:
        file.write(message)
    run(["./transfer_data.sh", filename])
