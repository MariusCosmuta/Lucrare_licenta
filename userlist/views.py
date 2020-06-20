from django.shortcuts import redirect
from .models import userlist
from anime_detail.models import  anime_detail
# Create your views here.


def userlist_all_anime(id):
    anime = anime_detail.objects.all()
    lista = userlist.objects.all()
    final = []
    for l in lista:
        if(id == l.user_id):
            for a in anime:
                if(a.anime_id == l.anime_id):
                    final.append([a, int(l.rating)])
    return final


def id_anime_for_recommander(id):
    lista = userlist.objects.all()
    final = []
    for l in lista:
        if(id == l.user_id):
            final.append(l.anime_id)
    return final


def add_to_animelist(request, id, like):
    userlist.objects.update_or_create(anime_id=id, user_id=request.user.id, rating=like)
    return redirect('/')


def add_to_animelist_recommendation(request, id, like):
    userlist.objects.update_or_create(anime_id=id, user_id=request.user.id, rating=like)
    return redirect('/recommendation_system')


def delete_to_animelist(request, anime_id):
    userlist.objects.get(anime_id=anime_id, user_id=request.user.id).delete()
    return redirect("/account")
