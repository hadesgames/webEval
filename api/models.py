from django import forms
from django.db import models

class Eval (models.Model):
    public_key = models.CharField(max_length = 32)
    private_key = models.CharField(max_length = 64)
    compat_factor = models.FloatField()
    
    name = models.CharField(max_length = 32)
    os = models.CharField(max_length = 32)
    updated = models.BooleanField(default = True)
    
    def __unicode__ (self):
        return self.id
    
    def client_encode (self, message):
        return
    
    def server_encode (self, message):
        return 
    
    def client_decode (self, message):
        return
    
    def server_decode (self, message):
        return "Login"
    
    
class CreateEvalForm (forms.ModelForm):
    class Meta:
        model = Eval
        exclude = ('public_key', 'private_key')