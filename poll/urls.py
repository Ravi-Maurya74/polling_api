from django.urls import path
from poll import views

urlpatterns = [
    path('', views.loadmain),
    path('createAdmin/', views.NewAdmin.as_view()),
    path('createSite/', views.NewSite.as_view()),
    path('createSiteAdmin/', views.NewSiteAdmin.as_view()),
    path('createVoter/', views.NewVoter.as_view()),
    path('createPoll/', views.NewPoll.as_view()),
    path('createChoice/', views.NewChoice.as_view()),
    path('vote/', views.vote),
    path('pollDetail/', views.pollDetail),
    path('pollSiteInfo/', views.pollSiteInfo),
    path('stopPoll/', views.stopPoll),
    path('startPoll/', views.startPoll),
    path('listPoll/', views.ListPoll.as_view()),
    path('localadmin/', views.siteadmin),
    path('administrator/', views.loadadminpg),
    path('candidates/', views.getCandidates),
]
