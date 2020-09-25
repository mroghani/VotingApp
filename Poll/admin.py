from django import forms
from django.contrib import admin
import secrets

from .models import Voter, Candidate, Vote

admin.site.register(Candidate)

class VoterAdminForm(forms.ModelForm):
    class Meta:
        model = Voter
        exclude = ['token']

    def save(self, commit=True):
        self.instance.token = secrets.token_hex(20)
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance


class VoterAdmin(admin.ModelAdmin):
    exclude = []
    form = VoterAdminForm
    list_display = ('email', 'token')


class VoteAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ['voter', 'candidate', ]


admin.site.register(Voter, VoterAdmin)
admin.site.register(Vote, VoteAdmin)
