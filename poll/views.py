from django.shortcuts import render
from .models import Poll, Choice, Voter, Site, SiteAdmin, Admin
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db.models import Q
from .serializer import CreateAdminSerializer, CreateSiteSerializer, CreateSiteAdminSerializer, CreateVoterSerializer, \
    CreatePollSerializer, CreateChoiceSerializer, VoterInfoSerializer, PollDetailSerializer, ChoiceSiteSerializer, PollInfoSerializer, PollCandidatesSerializer, CandidatesSerializer


# Create your views here.

class NewAdmin(generics.CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = CreateAdminSerializer


class NewSite(generics.CreateAPIView):
    queryset = Site.objects.all()
    serializer_class = CreateSiteSerializer


class NewSiteAdmin(generics.CreateAPIView):
    queryset = SiteAdmin.objects.all()
    serializer_class = CreateSiteAdminSerializer


class NewVoter(generics.CreateAPIView):
    queryset = SiteAdmin.objects.all()
    serializer_class = CreateVoterSerializer


class NewPoll(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = CreatePollSerializer


class NewChoice(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = CreateChoiceSerializer


def loadmain(request):
    return render(request, "index.html")


def loadadminpg(request):
    return render(request, "administrator.html")


def siteadmin(request):
    return render(request, "localadmin.html")


@api_view(['POST'])
def vote(request):
    received_json_data = json.loads(request.body)
    try:
        voter_instance = Voter.objects.get(email=received_json_data['email'])
    except:
        return Response({'prompt': 'Invalid email.'})
    if voter_instance.password != received_json_data['password']:
        return Response({'prompt': 'Invalid Password.'})
    choice_instance = Choice.objects.get(choice=received_json_data['choice'])
    poll_instance = Poll.objects.get(pk=received_json_data['poll_id'])
    if voter_instance.answered.contains(poll_instance):
        return Response({'status': 400, 'prompt': 'Already voted.'})
    if not poll_instance.isActive:
        return Response({'status': 400, 'prompt': 'Poll is over. Cannot vote now.'})
    choice_instance.votes += 1
    voter_instance.choices.add(choice_instance)
    voter_instance.answered.add(poll_instance)
    choice_instance.save()
    voter_instance.save()
    return Response({'status': 200, 'name': voter_instance.name, 'choice': choice_instance.choice})


@api_view(['POST'])
def pollDetail(request):
    received_json_data = json.loads(request.body)
    try:
        admin_instance = Admin.objects.get(email=received_json_data['email'])
    except:
        return Response(({'prompt': 'given email does not exist.'}))

    if (admin_instance.password != received_json_data['password']):
        return Response({'prompt': 'Invalid password.'})

    poll_instance = Poll.objects.get(pk=received_json_data['poll_id'])
    data = PollDetailSerializer(poll_instance).data
    return Response(data)


@api_view(['POST'])
def pollSiteInfo(request):
    received_json_data = json.loads(request.body)
    print(received_json_data)
    try:
        site_admin_instance = SiteAdmin.objects.get(
            email=received_json_data['email'])
    except:
        return Response({'prompt': 'given email does not exist.'})
    if site_admin_instance.password != received_json_data['password']:
        return Response({'prompt': 'Invalid.'})
    poll_instance = Poll.objects.get(pk=1)
    poll_data = PollDetailSerializer(poll_instance).data
    site_instance = site_admin_instance.site
    choices_instance = Choice.objects.filter(poll__exact=poll_instance)
    result_data = ChoiceSiteSerializer(choices_instance, many=True, context={
                                       'site_id': site_instance.id}).data
    return Response({'description': poll_data['description'], 'results': result_data})


@api_view(['POST'])
def startPoll(request):
    received_json_data = json.loads(request.body)
    poll_instance = Poll.objects.get(pk=received_json_data['poll_id'])
    poll_instance.isActive = True
    poll_instance.save()
    data = PollDetailSerializer(poll_instance).data
    return Response(data)


@api_view(['POST'])
def stopPoll(request):
    received_json_data = json.loads(request.body)
    poll_instance = Poll.objects.get(pk=received_json_data['poll_id'])
    poll_instance.isActive = False
    poll_instance.save()
    data = PollDetailSerializer(poll_instance).data
    return Response(data)


class ListPoll(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollInfoSerializer


@api_view(['POST'])
def getCandidates(request):
    received_json_data = json.loads(request.body)
    poll_instance = Poll.objects.get(pk=received_json_data['poll_id'])
    data = CandidatesSerializer(poll_instance.choices, many=True).data
    return Response(data)
