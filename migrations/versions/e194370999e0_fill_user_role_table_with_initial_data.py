"""Fill user_role table with initial data.

Revision ID: e194370999e0
Revises: 0ec1f621b940
Create Date: 2022-01-18 12:05:11.914515

"""
from alembic import op
import sqlalchemy as sa

from app.models import UserRole
from app import db

# revision identifiers, used by Alembic.
revision = 'e194370999e0'
down_revision = '0ec1f621b940'
branch_labels = None
depends_on = None


def upgrade():
    user = UserRole(role_name="Пользователь", role_codename="ordinary")
    admin = UserRole(role_name="Администратор", role_codename="admin")
    db.session.add(user)
    db.session.add(admin)
    db.session.commit()

def downgrade():
    pass
