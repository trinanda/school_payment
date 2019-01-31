import os

from flask_security.utils import encrypt_password

from app import db, app, Role, user_datastore


def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    db.drop_all()
    db.create_all()

    with app.app_context():
        super_user_role = Role(name='superuser')
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            name='superuser',
            email='superuser@example.com',
            password=encrypt_password('123456'),
            roles=[super_user_role]
        )

        db.session.commit()
    return


if __name__ == "__main__":
    # build a sample db on the fly, if one does not exist yet.
    database_path = app.config['DATABASE_FILE']
    if not os.path.exists(database_path):
        build_sample_db()
