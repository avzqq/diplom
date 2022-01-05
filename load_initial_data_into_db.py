import csv
from app.models import LocomotiveRepairPeriod
from app import db


def save_initial_data(row):
    model = LocomotiveRepairPeriod(
        loco_model_name=row["loco_model_name"],
        three_maintenance=row["three_maintenance"],
        one_current_repair=row["one_current_repair"],
        two_current_repair=row["two_current_repair"],
        three_current_repair=row["three_current_repair"],
        medium_repair=row["medium_repair"], overhaul=row["overhaul"]
    )
    db.session.add(model)
    db.session.commit()


def read_csv(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            save_initial_data(row)


if __name__ == "__main__":
    read_csv("initial_data.csv")
