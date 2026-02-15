"""Convert all id and FK fields from VARCHAR to UUID safely

Revision ID: 526868f6590e
Revises: 2eba57c88242
"""

from alembic import op
import sqlalchemy as sa


revision = "526868f6590e"
down_revision = "2eba57c88242"
branch_labels = None
depends_on = None


def upgrade():

    # --------------------------------------------------
    # 1️⃣ Drop ALL foreign key constraints
    # --------------------------------------------------

    op.drop_constraint("study_room_members_user_id_fkey",
                       "study_room_members", type_="foreignkey")
    op.drop_constraint("study_room_members_study_room_id_fkey",
                       "study_room_members", type_="foreignkey")

    op.drop_constraint("study_rooms_created_by_fkey",
                       "study_rooms", type_="foreignkey")

    op.drop_constraint("study_materials_room_id_fkey",
                       "study_materials", type_="foreignkey")
    op.drop_constraint("study_materials_uploaded_by_fkey",
                       "study_materials", type_="foreignkey")

    op.drop_constraint("study_material_reports_material_id_fkey",
                       "study_material_reports", type_="foreignkey")
    op.drop_constraint("study_material_reports_reported_by_fkey",
                       "study_material_reports", type_="foreignkey")

    # --------------------------------------------------
    # 2️⃣ Convert PRIMARY KEY columns first
    # --------------------------------------------------

    op.execute("""
        ALTER TABLE users
        ALTER COLUMN id TYPE UUID USING id::uuid
    """)

    op.execute("""
        ALTER TABLE study_rooms
        ALTER COLUMN id TYPE UUID USING id::uuid
    """)

    op.execute("""
        ALTER TABLE study_materials
        ALTER COLUMN id TYPE UUID USING id::uuid
    """)

    op.execute("""
        ALTER TABLE study_room_members
        ALTER COLUMN id TYPE UUID USING id::uuid
    """)

    op.execute("""
        ALTER TABLE study_material_reports
        ALTER COLUMN id TYPE UUID USING id::uuid
    """)

    # --------------------------------------------------
    # 3️⃣ Convert FOREIGN KEY columns
    # --------------------------------------------------

    op.execute("""
        ALTER TABLE study_room_members
        ALTER COLUMN user_id TYPE UUID USING user_id::uuid
    """)

    op.execute("""
        ALTER TABLE study_room_members
        ALTER COLUMN study_room_id TYPE UUID USING study_room_id::uuid
    """)

    op.execute("""
        ALTER TABLE study_rooms
        ALTER COLUMN created_by TYPE UUID USING created_by::uuid
    """)

    op.execute("""
        ALTER TABLE study_materials
        ALTER COLUMN room_id TYPE UUID USING room_id::uuid
    """)

    op.execute("""
        ALTER TABLE study_materials
        ALTER COLUMN uploaded_by TYPE UUID USING uploaded_by::uuid
    """)

    op.execute("""
        ALTER TABLE study_material_reports
        ALTER COLUMN material_id TYPE UUID USING material_id::uuid
    """)

    op.execute("""
        ALTER TABLE study_material_reports
        ALTER COLUMN reported_by TYPE UUID USING reported_by::uuid
    """)

    # --------------------------------------------------
    # 4️⃣ Recreate FOREIGN KEY constraints
    # --------------------------------------------------

    op.create_foreign_key(
        "study_room_members_user_id_fkey",
        "study_room_members",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_room_members_study_room_id_fkey",
        "study_room_members",
        "study_rooms",
        ["study_room_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_rooms_created_by_fkey",
        "study_rooms",
        "users",
        ["created_by"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_materials_room_id_fkey",
        "study_materials",
        "study_rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_materials_uploaded_by_fkey",
        "study_materials",
        "users",
        ["uploaded_by"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_material_reports_material_id_fkey",
        "study_material_reports",
        "study_materials",
        ["material_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "study_material_reports_reported_by_fkey",
        "study_material_reports",
        "users",
        ["reported_by"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    raise Exception("Downgrade not supported for UUID migration.")
