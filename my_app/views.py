from django.shortcuts import render
from anime_detail.models import anime_detail as anime
from django.core.paginator import Paginator
from userlist.views import *
import operator
#from Algoritm.Algoritm import recommendation_system as rs
#from Algoritm.Algoritm import get_item_recommendations
# Create your views here.


def anime_object():
    return anime.objects.all()


def home(request):
    if (request.user):
        title = []
        ids = id_anime_for_recommander(request.user.id)
        for anime in anime_detail.objects.order_by('popularity'):
            contor = True
            for id in ids:
                if(anime.anime_id==id):
                    contor = False
                    ids.remove(id)
            if(contor):
                title.append(anime)
    else:
        title = anime_detail.objects.order_by('popularity')
    paginator = Paginator(title, 50)
    page = request.GET.get('page')
    title = paginator.get_page(page)
    stuff_for_frontend = {
        'title': title,
    }
    return render(request, 'my_app/animelist.html', stuff_for_frontend)


def search(request):
    nume = list()
    animelist = anime_object()
    if request.method == "POST":
        cautare = request.POST['anime']
        for anime in animelist:
            if(cautare in anime.title):
                nume.append(anime)
    stuff_for_frontend = {
        'title': nume,
    }
    return render(request, 'my_app/search.html', stuff_for_frontend)


def search_genre(request, genre):
    title = anime.objects.all()
    new_genre = ''
    for g in genre:
        if(g =='_'):
            new_genre += ' '
        else:
            new_genre += g
    final = []
    for t in title:
        gen = t.genre.split(', ')
        for g in gen:
            if( g == new_genre):
                final.append(t)
    stuff_for_frontend = {
        'title': final,
    }
    return render(request, "my_app/search.html", stuff_for_frontend)


def account(request):
    message = "Change Password"
    if(request.POST):
        if(request.user.check_password(request.POST['oldpassword'])):
            if(request.POST['newpassword1'] == request.POST['newpassword2']):
                request.user.set_password(request.POST['newpassword1'])
                request.user.save()
                message = 'Password changed successfully '
            else:
                message = 'You need to write the same password'
        else:
            message = 'Old password is wrong'
    return render(request, 'my_app/account.html', {'message': message, 'anime': userlist_all_anime(request.user.id), })


def list_with_animes(animes_id, lista):
    list_animes = []
    test = []
    if(type(lista[0]) != int):
        for i in lista:
            test.append(i.anime_id)
    else:
        test = [10000000,12111111]
    for id in animes_id:
        if((id in test) == False):
            list_animes.append(anime_detail.objects.get(anime_id=id))
    return list_animes[:30]


def recommendation_system(request):
    if request.method == "POST":
        c = get_item_recommendations(request.POST['anime'], k=30)
        c = c['Anime_ID']
        return render(request, 'my_app/recommendation_system.html', {'anime': list_with_animes(c, [10000000,12111111])})

    if (request.user.is_authenticated):
        lista = []
        lista2 = []
        for uid in userlist.objects.all():
            if(uid.user_id == request.user.id and uid.rating == True):
                lista.append(anime_detail.objects.get(anime_id=uid.anime_id))
            elif (uid.user_id == request.user.id and uid.rating == False):
                lista2.append(anime_detail.objects.get(anime_id=uid.anime_id))
        if(len(lista) > 4):
            animes = rs(lista)
            for l in lista2:
                lista.append(l)
            return render(request, 'my_app/recommendation_system.html', {'anime': list_with_animes(animes, lista)})
    return render(request, 'my_app/recommendation_system.html')

    anime_list = rs(id_anime_for_recommander(request.user.id))
    final = []
    for anime in anime_detail.objects.all():
        if(anime.anime_id in anime_list):
            final.append(anime)
    return render(request, 'my_app/recommendation_system.html', {"anime": final})

'''
def recommendation_system(request):
    if request.method == "POST":
        c = get_item_recommendations(request.POST['anime'], k=30)
    else:
        c = get_item_recommendations('Dragon Ball Z', k=30)
    stuff_for_frontend = {
        'id': c['Anime_ID'],
        'title': c['title'],
        'genre': c['genre'],
    }
    return render(request, 'my_app/recommendation_system.html', stuff_for_frontend)
'''