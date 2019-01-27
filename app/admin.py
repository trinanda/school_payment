import flask_admin
from flask import url_for
from flask_admin import helpers as admin_helpers

from app import app, db, security
from app.models import Student, Bill, Role, Parent, School
from app.modelview import StudentModelView, BillModelView, RoleModelView, ParentModelView, \
    SchoolModelView, ParentView

admin = flask_admin.Admin(app, '#',
                          base_template='my_master.html',
                          template_mode='bootstrap3')

# Add model views
admin.add_view(StudentModelView(Student, db.session))
admin.add_view(BillModelView(Bill, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(ParentModelView(Parent, db.session))
admin.add_view(SchoolModelView(School, db.session))
admin.add_view(ParentView(name='Your Children Bill', endpoint='yourchildrendbill'))


# define a context processor for merging flask-admin's template context into the flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
