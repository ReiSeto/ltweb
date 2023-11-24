from view.base_model_view import BaseModelView
from wtforms import PasswordField


class AccountView(BaseModelView):
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, adminn, is_created):
        if form.password.data:
            adminn.set_password(form.password.data)
            print("Set password successfully")

