from django.contrib import admin
from .models import Voter, Choice, Poll, Admin, SiteAdmin, Site


# Register your models here
class SiteView(admin.ModelAdmin):
    readonly_fields = ('id', 'admin', 'voter',)

    def voter(self, instance):
        return [v.name for v in instance.voter.all()]


class PollView(admin.ModelAdmin):
    readonly_fields = ('choices',)

    def choices(self, instance):
        return [f'{c.choice}: {c.votes}' for c in instance.choices.all()]


admin.site.register(Voter)
admin.site.register(Choice)
admin.site.register(Poll, PollView)
admin.site.register(Admin)
admin.site.register(Site, SiteView)
admin.site.register(SiteAdmin)
