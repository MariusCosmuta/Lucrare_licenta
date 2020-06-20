from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import anime_detail
import pandas as pd



@permission_required('admin.can_add_log_entry')
def upload_csv(request):
    template = "my_app/upload_csv.html"
    prompt = {
        'order': 'Order of the csv should be anime_id, title, title_english, title_synonyms, image_url, type, sourse, '
                 'status, airing, aired, duration, score, sored_by, rank, popularity, members, favorites, background,'
                 'premiered, producer, licensor, studio, genre, duration_min',
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    #data_set = csv_file.read().decode('UTF-8')
    #io_string = io.StringIO(data_set)

    #next(io_string)
    ScoresDF = pd.read_csv(csv_file)

    ScoresDF = ScoresDF[['anime_id', 'title', 'title_english', 'title_synonyms', 'image_url', 'type', 'source', 'status', 'airing', 'aired', 'duration', 'score', 'scored_by', 'rank', 'popularity', 'members', 'favorites', 'background', 'premiered', 'producer', 'licensor', 'studio', 'genre', 'duration_min']]
    for i in range(len(ScoresDF)):
        _, created = anime_detail.objects.update_or_create(
            anime_id=ScoresDF['anime_id'][i],
            title=ScoresDF['title'][i],
            title_english=ScoresDF['title_english'][i],
            title_synonyms=ScoresDF['title_synonyms'][i],
            image_url="https://cdn.myanimelist.net/" + ScoresDF['image_url'][i][33:],
            type=ScoresDF['type'][i],
            source=ScoresDF['source'][i],
            status=ScoresDF['status'][i],
            airing=ScoresDF['airing'][i],
            aired=ScoresDF['aired'][i],
            duration=ScoresDF['duration'][i],
            score=ScoresDF['score'][i],
            scored_by=ScoresDF['scored_by'][i],
            rank=ScoresDF['rank'][i],
            popularity=ScoresDF['popularity'][i],
            members=ScoresDF['members'][i],
            favorites=ScoresDF['favorites'][i],
            background=ScoresDF['background'][i],
            premiered=ScoresDF['premiered'][i],
            producer=ScoresDF['producer'][i],
            licensor=ScoresDF['licensor'][i],
            studio=ScoresDF['studio'][i],
            genre=ScoresDF['genre'][i],
            duration_min=ScoresDF['duration_min'][i],
        )
    return render(request, template)