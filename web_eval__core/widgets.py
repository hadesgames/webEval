# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode
from django.conf import settings
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
import datetime, time
from dateutil import parser
from recaptcha.client import captcha

# DATETIMEWIDGET
calbtn = u"""<img src="%simages/calbutton.gif" alt="calendar" id="%s_btn" style="cursor: pointer; border: 1px solid #8888aa;" title="Select date and time"
            onmouseover="this.style.background='#444444';" onmouseout="this.style.background=''" />
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "%s",
        ifFormat       :    "%s",
        button         :    "%s_btn",
        singleClick    :    true,
        showsTime      :    true
    });
</script>"""

class DateTimeWidget(forms.widgets.TextInput):
    dformat = '%Y-%m-%d %H:%M'
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '': 
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']
        
        jsdformat = self.dformat #.replace('%', '%%')
        cal = calbtn % (settings.MEDIA_URL, id, id, jsdformat, id)
        a = u'<input%s />%s' % (forms.util.flatatt(final_attrs), cal)
        return mark_safe(a)

    def value_from_datadict(self, data, files, name):
        dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        empty_values = forms.fields.EMPTY_VALUES

        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        for format in dtf:
            try:
                return datetime.datetime(*time.strptime(value, format)[:6])
            except ValueError:
                continue
        return None
    
    
class ParseDateTimeField(forms.Field):
    """ DateTime field that accepts natural-language input

    Uses the DateUtil module to parse input.

    """
    def clean(self, value):
        super(ParseDateTimeField, self).clean(value)
        if value in (None, ''):
            return None
        if isinstance(value, datetime):
            return value
        try:
            return parser.parse(value)
        except ValueError:
            raise ValidationError(u'Enter a valid date and time')


class ParseDateField(forms.Field):
    """ Date field that accepts natural-language input

    Uses the DateUtil module to parse input.

    """
    def clean(self, value):
        super(ParseDateField, self).clean(value)
        if value in (None, ''):
            return None
        if isinstance(value, datetime):
            return value
        try:
            return parser.parse(value).date()
        except ValueError:
            raise ValidationError(u'Enter a valid date')

def parsefield_callback(field, **kwargs):
    """ Replace standard DateField and DateTimeField with parsing variants """
    if isinstance(field, models.DateTimeField):
        kwargs.update({'form_class': ParseDateTimeField})
    elif isinstance(field, models.DateField):
        kwargs.update({'form_class': ParseDateField})
    return field.formfield(**kwargs)

    
class ReCaptcha(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None), 
            data.get(self.recaptcha_response_name, None)]
