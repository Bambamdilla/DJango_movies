from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from django.forms import CharField, Form, Textarea

class SubmittableForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(*self.fields, Submit('submit', 'Submit'))