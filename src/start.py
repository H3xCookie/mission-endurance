import sys
from datetime import datetime
from subprocess import run

import read_config_files

if __name__ == "__main__":
    job_path = "J000001"
    passes = {
        "pass_1": {
            "time_filename": "Time_1.txt",
            "field_filename": "field_coords_1.csv",
            "ground_kpts": "ground_keypoints_10_10_1.pkl",
        },
        "pass_2": {
            "time_filename": "Time_2.txt",
            "field_filename": "field_coords_2.csv",
            "ground_kpts": "ground_keypoints_10_10_2.pkl",
        },
    }
    passes_in_future = []
    time_of_program_starting = datetime.utcnow().timestamp()
    for p in passes:
        time_filename = passes[p]["time_filename"]
        utc_time_of_pass = read_config_files.time_of_photo(time_filename)
        if time_of_program_starting < utc_time_of_pass - 5:
            passes_in_future.append(p)

    if len(passes_in_future) == 0:
        print("started too late, all planned passes are in the past now")
        sys.exit("too late to start main fn")
    else:
        our_pass = passes[passes_in_future[0]]
        run(
            [
                "python3",
                "main.py",
                "--time_filename",
                our_pass["time_filename"],
                "--field_filename",
                our_pass["field_filename"],
                "--ground_kpts",
                our_pass["ground_kpts"],
                "--job_path",
                job_path,
            ]
        )
