from rest_framework import serializers
from .models import Poll, Choice, Voter, Site, SiteAdmin, Admin


class CreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'name',
            'email',
            'password',
        ]


class CreateSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            'site_name',
        ]


class CreateSiteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAdmin
        fields = [
            'name',
            'email',
            'password',
            'site',
        ]


class CreatePollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'description'
        ]


class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'choice',
            'poll',
        ]


class CreateVoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            'name',
            'email',
            'password',
            'site',
        ]


class VoterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = [
            'id',
            'name',
            'email',
            'site',
            'choices',
        ]


class PollDetailSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(read_only=True)

    def get_results(self, instance):
        result_list = []
        for ch in instance.choices.all():
            result_list.append({'choice': ch.choice, 'count': ch.votes})
        return result_list

    class Meta:
        model = Poll
        fields = [
            'description',
            'isActive',
            'results'
        ]


class ChoiceSiteSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Choice
        fields = [
            'choice',
            'count',
        ]

    def get_count(self, instance):
        site_id = self.context.get('site_id')
        site_instance = Site.objects.get(pk=site_id)
        voters_instance = Voter.objects.filter(site__exact=site_instance).filter(choices=instance)
        # choices will be a list of many choices but writing choices=instance compares all choice
        # choices with instance.
        return voters_instance.count()


class PollInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'description',
            'isActive'
        ]
