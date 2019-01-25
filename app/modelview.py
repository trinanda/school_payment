import random
import string

from flask import abort, redirect, url_for, request
from flask_admin.contrib import sqla
from sqlalchemy import func
from flask_security import current_user
from app.models import Student


def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class SuperUserModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class SchoolAdminModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('schooladmin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class ParentModelView(SchoolAdminModelView):
    pass


class StudentModelView(SchoolAdminModelView):
    def get_query(self):
        # return Student.query.filter_by(school_id=current_user.id)
        return self.session.query(self.model).filter(
            Student.school_id == current_user.id
        )

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model).filter(
            Student.school_id == current_user.id
        )

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.school_id = current_user.id
            model.student_registration_number = generator_random()

    form_excluded_columns = ('student_registration_number')

class BillModelView(SchoolAdminModelView):
    column_list = ('student_id', 'total_bill', 'bill_status')
    pass


class RoleModelView(SuperUserModelView):
    pass


class UserModelView(SuperUserModelView):
    pass
