import random
import string

from flask import abort, redirect, url_for, request
from flask_admin import expose, BaseView, AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.model import BaseModelView
from sqlalchemy import func
from flask_security import current_user

from app import db
from app.models import Student, Parent, BillStatus, Bill


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
        if current_user.has_role('school'):
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


class StudentModelView(SchoolAdminAccess):
    # form_columns = ['name', 'major']
    column_exclude_list = ('created_at', 'updated_at')
    edit_modal = True
    create_modal = True
    can_view_details = True
    details_modal = True
    form_excluded_columns = ('student_registration_number', 'created_at', 'updated_at', 'Bill')

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
    column_list = ('student', 'total_bill', 'bill_status', 'created_at', 'updated_at')
    form_excluded_columns = ('created_at', 'updated_at', 'bill_status')
    edit_modal = True
    create_modal = True
    can_view_details = True
    details_modal = True
    can_edit = False

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.bill_status = BillStatus.PENDING.value
            model.school_id = current_user.id

    def get_query(self):
        # return Student.query.filter_by(school_id=current_user.id)
        return self.session.query(self.model).filter(
            Bill.school_id == current_user.id
        )

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model).filter(
            Bill.school_id == current_user.id
        )

    # can_create = False
    # can_delete = False
    # can_export = True
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
    column_list = ('name', 'email', 'roles', 'active', 'created_at', 'updated_at')
    form_excluded_columns = ('created_at', 'updated_at')
    column_exclude_list = ('password')

    # form_columns = ['roles', 'id', 'email', 'password', 'active']

    edit_modal = True
    create_modal = True
    can_view_details = True
    details_modal = True


class ParentModelView(SchoolAdminAccess):
    form_excluded_columns = ('created_at', 'updated_at', 'roles')
    column_exclude_list = ('password')
    edit_modal = True
    create_modal = True
    can_view_details = True
    details_modal = True

    def get_query(self):
        return self.session.query(self.model).filter(
            Parent.school_id == current_user.id
        )

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model).filter(
            Parent.school_id == current_user.id
        )

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.school_id = current_user.id


class SchoolModelView(SuperUseAccess):
    column_list = ('name', 'email', 'roles', 'active')
    form_excluded_columns = ('created_at', 'updated_at')
    column_exclude_list = ('password')

    edit_modal = True
    create_modal = True
    can_view_details = True
    details_modal = True


class ParentView(BaseView):
    @expose('/')
    def index(self):
        data = 'test123123'
        student = db.session.query(Student).filter_by(parent_id=current_user.id).all()
        print('test', student)
        # student = student.name
        return self.render('admin/index.html', student=student)

