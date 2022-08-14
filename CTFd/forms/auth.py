from wtforms import PasswordField, StringField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import (
    attach_custom_user_fields,
    attach_registration_code_field,
    build_custom_user_fields,
    build_registration_code_field,
)
# CSAW Regions
# Not pretty, but works for now
regions = [("US-Canada", "United States"), ("US-Canada", "Canada"), ("US-Canada", "American Samoa"), ("US-Canada", "Guam"), ("US-Canada", "Northern Mariana Islands"), ("US-Canada", "Puerto Rico"), ("US-Canada", "US Virgin Islands"), ("Mexico", "Mexico"), ("India", "India"), ("Mena", "Algeria"), ("Mena", "Azerbaijan"), ("Mena", "Bahrain"), ("Mena", "Chad"), ("Mena", "Djibouti"), ("Mena", "Egypt"), ("Mena", "Eritrea"), ("Mena", "Georgia"), ("Mena", "Jordan"), ("Mena", "Iraq"), ("Mena", "Iran"), ("Mena", "Israel"), ("Mena", "Kuwait"), ("Mena", "Lebanon"), ("Mena", "Libya"), ("Mena", "Mauritania"), ("Mena", "Morocco"), ("Mena", "Oman"), ("Mena", "Pakistan"), ("Mena", "Palestine"), ("Mena", "Qatar"), ("Mena", "Saudi Arabia"), ("Mena", "South Sudan"), ("Mena", "Sudan"), ("Mena", "Syria"), ("Mena", "Tunisia"), ("Mena", "Turkey"), ("Mena", "United Arab Emirates"), ("Mena", "Yemen"), ("Europe", "Armenia"), ("Europe", "Norway"), ("Europe", "Switzerland"), ("Europe", "United Kingdom"), ("Europe", "Austria"), ("Europe", "Italy"), ("Europe", "Belgium"), ("Europe", "Latvia"), ("Europe", "Bulgaria"), ("Europe", "Lithuania"), ("Europe", "Croatia"), ("Europe", "Luxembourg"), ("Europe", "Cyprus"), ("Europe", "Malta"), ("Europe", "Czechia"), ("Europe", "Netherlands"), ("Europe", "Denmark"), ("Europe", "Poland"), ("Europe", "Estonia"), ("Europe", "Portugal"), ("Europe", "Finland"), ("Europe", "Romania"), ("Europe", "France"), ("Europe", "Slovakia"), ("Europe", "Germany"), ("Europe", "Slovenia"), ("Europe", "Greece"), ("Europe", "Spain"), ("Europe", "Hungary"), ("Europe", "Sweden"), ("Europe", "Ireland")]

bracket_choices = ["Undergraduate", "Graduate", "Stacked"]

def RegistrationForm(*args, **kwargs):
    class _RegistrationForm(BaseForm):
        name = StringField("User Name", validators=[InputRequired()])
        email = EmailField("Email", validators=[InputRequired()])
        password = PasswordField("Password", validators=[InputRequired()])
        region = SelectField("Region", choices=regions, validators=[InputRequired()])
        # There is already something called bracket 
        brack = SelectField("Bracket", choices=bracket_choices, validators=[InputRequired()])
        submit = SubmitField("Submit")

        @property
        def extra(self):
            return build_custom_user_fields(
                self, include_entries=False, blacklisted_items=()
            ) + build_registration_code_field(self)

    attach_custom_user_fields(_RegistrationForm)
    attach_registration_code_field(_RegistrationForm)

    return _RegistrationForm(*args, **kwargs)


class LoginForm(BaseForm):
    name = StringField("User Name or Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ConfirmForm(BaseForm):
    submit = SubmitField("Resend Confirmation Email")


class ResetPasswordRequestForm(BaseForm):
    email = EmailField("Email", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ResetPasswordForm(BaseForm):
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Submit")
