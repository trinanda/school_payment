import random
import string

from flask import abort, redirect, url_for, request
from flask_admin import expose, BaseView
from flask_admin.contrib import sqla
from flask_admin.model.template import EndpointLinkRowAction
from sqlalchemy import func
from flask_security import current_user
from werkzeug.security import generate_password_hash

from app.models import Student


def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class SuperUseAccess(sqla.ModelView):

    form_excluded_columns = ('created_at', 'updated_at')

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


class SchoolAdminAccess(sqla.ModelView):

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


# class ParentModelView(SchoolAdminAccess):
#
#     form_excluded_columns = ('created_at', 'updated_at')
#
#     # def on_model_change(self, form, model, is_created):
#     #     if form.password_hash.data:
#     #         model.password_hash = generate_password_hash(form.password_hash.data)


class StudentModelView(SchoolAdminAccess):

    form_excluded_columns = ('student_registration_number', 'created_at', 'updated_at')

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


class BillModelView(SchoolAdminAccess):
    column_list = ('student_id', 'total_bill')

    # can_create = False
    # can_edit = False
    # can_delete = False
    # list_template = './templates/index.html'
    # can_export = True
    # edit_modal = True
    # create_modal = True
    # can_view_details = True
    # details_modal = True
    #
    # column_editable_list = ['total_bill']
    # column_searchable_list = column_editable_list
    # column_exclude_list = ['total_bill']
    # form_excluded_columns = column_exclude_list
    # column_details_exclude_list = column_exclude_list
    # column_filters = column_editable_list


class RoleModelView(SuperUseAccess):
    pass


class UserModelView(SuperUseAccess):
    pass
