"""
An easy-to-use Django forms integration of the reCaptcha service.
v1.0.1

To use, simply base your form off the ``RecaptchaForm`` class. This class adds
a new argument that must be provided to the form, ``remote_ip``.

Two settings which must be set in your project's ``settings`` module are 
``RECAPTCHA_PUBLIC_KEY`` and ``RECAPTCHA_SECRET_KEY``, the public and private
keys for your domain, respectively. 

Following is an example of creating a basic comment form class and then
using an instance of the form in a view::

    from django import forms
    from mysite.utils import recaptcha

    class CommentForm(recaptcha.RecaptchaForm):
        name = forms.CharField()
        comment = forms.CharField(widget=Textarea())
        captcha = recaptcha.RecaptchaField()

    def comment(request):
        comment_form = CommentForm(remote_ip=request.META['REMOTE_ADDR'])
        ...

If you need to use a different base form (such as ``ModelForm``), use multiple
inheritance like so::

    class MyModelForm(BaseRecaptchaForm, ModelForm):
        ...
"""

import httplib
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.http import urlencode

OPTIONS_SCRIPT_HTML = u'''<script type="text/javascript">
   var RecaptchaOptions = %r;
</script>
'''
RECAPTCHA_HTML = u'''%(options)s<script type="text/javascript" src="http://api.recaptcha.net/challenge?k=%(public_key)s"></script>
<noscript>
   <iframe src="http://api.recaptcha.net/noscript?k=%(public_key)s"
       height="300" width="500" frameborder="0"></iframe><br />
   <textarea name="recaptcha_challenge_field" rows="3" cols="40">
   </textarea>
   <input type="hidden" name="recaptcha_response_field" value="manual_challenge" />
</noscript>'''


class RecaptchaWidget(forms.Widget):
    def __init__(self, theme=None, tabindex=None, public_key=None):
        '''
        From http://recaptcha.net/apidocs/captcha/client.html#look-n-feel::

            theme:      'red' | 'white' | 'blackglass' | 'clean'
    
                Defines which theme to use for reCAPTCHA.
    
            tabindex:   any integer
    
                Sets a tabindex for the reCAPTCHA text box. If other elements
                in the form use a tabindex, this should be set so that
                navigation is easier for the user.
            
        The optional ``public_key`` argument can be used to override the
        default use of the project-wide ``RECAPTCHA_PUBLIC_KEY`` setting.
        '''
        options = {}
        if theme:
            options['theme'] = theme
        if tabindex:
            options['tabindex'] = tabindex
        self.options = options
        self.public_key = public_key or settings.RECAPTCHA_PUBLIC_KEY
        super(RecaptchaWidget, self).__init__()

    def render(self, name, value, attrs=None):
        args = dict(public_key=self.public_key, options='')
        if self.options:
            args['options'] = OPTIONS_SCRIPT_HTML % self.options
        return mark_safe(RECAPTCHA_HTML % args)

    def value_from_datadict(self, data, files, name):
        challenge = data.get('recaptcha_challenge_field')
        response = data.get('recaptcha_response_field')
        return (challenge, response)

    def id_for_label(self, id_):
        return None


class RecaptchaField(forms.Field):
    widget = RecaptchaWidget
    default_error_messages = {
        'required': u'Please enter the CAPTCHA solution.',
        'invalid': u'An incorrect CAPTCHA solution was entered.',
        'no-remote-ip': u'CAPTCHA failed due to no visible IP address.',
        'challenge-error': u'An error occurred with the CAPTCHA service - try '
            'refreshing.',
        'unknown-error': u'The CAPTCHA service returned the following error: '
            '%(code)s.',
    }

    def __init__(self, private_key=None, *args, **kwargs):
        """
        The optional ``private_key`` argument can be used to override the
        default use of the project-wide ``RECAPTCHA_SECRET_KEY`` setting.
        """
        self.remote_ip = None
        self.private_key = private_key or settings.RECAPTCHA_SECRET_KEY
        super(RecaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not self.remote_ip:
            raise forms.ValidationError(self.error_messages['no-remote-ip'])
        value = super(RecaptchaField, self).clean(value)
        challenge, response = value
        if not challenge:
            raise forms.ValidationError(self.error_messages['challenge-error'])
        if not response:
            raise forms.ValidationError(self.error_messages['required'])
        try:
            value = validate_recaptcha(self.remote_ip, challenge, response,
                                       self.private_key)
        except RecaptchaError, e:
            if e.code == 'incorrect-captcha-sol':
                raise forms.ValidationError(self.error_messages['invalid'])
            raise forms.ValidationError(self.error_messages['unknown-error'] %
                                        {'code': e.code})
        return value


class BaseRecaptchaForm(forms.BaseForm):
    def __init__(self, remote_ip, *args, **kwargs):
        super(BaseRecaptchaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, RecaptchaField):
                field.remote_ip = remote_ip


class RecaptchaForm(BaseRecaptchaForm, forms.Form):
    pass


class RecaptchaError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code


def validate_recaptcha(remote_ip, challenge, response, private_key):
    assert challenge, 'No challenge was provided for reCaptcha validation'
    # Request validation from recaptcha.net
    params = dict(privatekey=private_key, remoteip=remote_ip,
                  challenge=challenge, response=response)
    params = urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api-verify.recaptcha.net")
    conn.request("POST", "/verify", params, headers)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
    else:
        data = ''
    conn.close()
    # Validate based on response data
    result = data.startswith('true')
    if not result:
        bits = data.split('\n', 2)
        error_code = ''
        if len(bits) > 1:
            error_code = bits[1]
        raise RecaptchaError(error_code)
    # Return dictionary
    return result
