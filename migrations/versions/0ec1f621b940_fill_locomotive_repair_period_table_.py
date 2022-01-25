"""Fill locomotive_repair_period table with initial data.

Revision ID: 0ec1f621b940
Revises: 5c27b8115c46
Create Date: 2022-01-18 12:03:15.996943

"""
from alembic import op
import sqlalchemy as sa

from app.models import LocomotiveRepairPeriod
from app import db

# revision identifiers, used by Alembic.
revision = '0ec1f621b940'
down_revision = '5c27b8115c46'
branch_labels = None
depends_on = None


def upgrade():
    tam = {"loco_model_name": "ТЭМ"}
    tam2y = {"loco_model_name": "ТЭМ2У"}
    tam2m = {"loco_model_name": "ТЭМ2М"}
    tam2ym = {"loco_model_name": "ТЭМ2УМ"}
    tam15 = {"loco_model_name": "ТЭМ15"}
    tam18 = {"loco_model_name": "ТЭМ18"}

    tgm4_a = {"loco_model_name": "ТГМ4(А)"}
    tgm4 = {"loco_model_name": "ТГМ4"}
    tgm4a = {"loco_model_name": "ТГМ4А"}

    tgm4_b = {"loco_model_name": "ТГМ4(Б)"}
    tgm4b = {"loco_model_name": "ТГМ4Б"}
    tgm4bl = {"loco_model_name": "ТГМ4Бл"}

    group_a = [tam, tam2y, tam2m, tam2ym, tam15, tam18]
    group_b = [tgm4_a, tgm4, tgm4a]
    group_c = [tgm4_b, tgm4b, tgm4bl]

    three_maintenance = {"0": 30}
    one_current_repair = {"0": 225, "1": 180}
    two_current_repair = {"0": 450, "1": 540, "2": 900}
    three_current_repair = {"0": 900, "1": 1080, "2": 1800}
    medium_repair = {"0": 2160, "1": 2700}
    overhaul = {"0": 4320, "1": 5400}

    for loco in group_a:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["0"]
        loco["two_current_repair"] = two_current_repair["0"]
        loco["three_current_repair"] = three_current_repair["0"]
        loco["medium_repair"] = medium_repair["0"]
        loco["overhaul"] = overhaul["0"]

    for loco in group_b:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["1"]
        loco["two_current_repair"] = two_current_repair["1"]
        loco["three_current_repair"] = three_current_repair["1"]
        loco["medium_repair"] = medium_repair["0"]
        loco["overhaul"] = overhaul["0"]

    for loco in group_c:
        loco["three_maintenance"] = three_maintenance["0"]
        loco["one_current_repair"] = one_current_repair["1"]
        loco["two_current_repair"] = two_current_repair["2"]
        loco["three_current_repair"] = three_current_repair["2"]
        loco["medium_repair"] = medium_repair["1"]
        loco["overhaul"] = overhaul["1"]

    all_data = [*group_a, *group_b, *group_c]
    for row in all_data:
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

def downgrade():
    pass
