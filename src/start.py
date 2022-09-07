from datetime import datetime

if __name__ == "__main__":
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
    time_of_starting = datetime.utcnow().timestamp()
