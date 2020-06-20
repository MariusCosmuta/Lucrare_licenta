import pandas as pd
import surprise as sp
import time

secunde = time.time()

UsersDF = pd.read_csv('C:/Users/Marius-PavelCosmuta/Desktop/Lucrare_licenta/Algoritm/users_cleaned.csv')
AnimesDF = pd.read_csv('C:/Users/Marius-PavelCosmuta/Desktop/Lucrare_licenta/Algoritm/anime_cleaned.csv')
ScoresDF = pd.read_csv('C:/Users/Marius-PavelCosmuta/Desktop/Lucrare_licenta/Algoritm/animelists_cleaned.csv')

ScoresDF = ScoresDF[['username', 'anime_id', 'my_score', 'my_status']]


ScoresDF['my_score'].describe().apply(lambda x: format(x, '.2f')).reset_index()

UsersAndScores = ScoresDF['username'].value_counts().reset_index().rename(columns={"username": "animes_rated", "index": "username"})

UsersSampled = UsersDF.sample(frac=.01, random_state=2)

UsersAndScoresSampled = pd.merge(UsersAndScores, UsersSampled, left_on = 'username', right_on = 'username', how = 'inner')

RatedsPerAnime = ScoresDF['anime_id'].value_counts().reset_index().rename(columns={"anime_id": "number_of_users", "index": "anime_id"})

UserRatedsCutten = UsersAndScoresSampled[UsersAndScoresSampled['animes_rated'] >= 10]
AnimeRatedsCutten = RatedsPerAnime[RatedsPerAnime['number_of_users'] >= 10]
ScoresDFHotStart = pd.merge(ScoresDF, UserRatedsCutten, left_on = 'username', right_on = 'username', how = 'inner')
ScoresDFHotStart = pd.merge(ScoresDFHotStart, AnimeRatedsCutten, left_on = 'anime_id', right_on = 'anime_id', how = 'inner')


als_param_grid = {'bsl_options': {'method': ['als'],
                              'reg_i': [5, 10, 15],
                              'reg_u': [10, 15, 20],
                              'n_epochs': [5, 10, 15, 20]
                              }
              }

sgd_param_grid = {'bsl_options': {'method': ['sgd'],
                              'reg': [0.01, 0.02, 0.03],
                              'n_epochs': [5, 10, 15, 20],
                              'learning_rate' : [0.001, 0.005, 0.01]
                              }
              }

als_gs = sp.model_selection.GridSearchCV(sp.BaselineOnly, als_param_grid, measures=['rmse'], cv = 3, joblib_verbose = 0)

sgd_gs = sp.model_selection.GridSearchCV(sp.BaselineOnly, sgd_param_grid, measures=['rmse'], cv = 3, joblib_verbose = 0)


reader = sp.Reader(rating_scale=(0, 10))
data = sp.Dataset.load_from_df(ScoresDFHotStart[['username', 'anime_id', 'my_score']], reader)
als_gs.fit(data)


sgd_gs.fit(data)

trainset = data.build_full_trainset()
algo = sp.BaselineOnly()
algo.fit(trainset)
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

last_predictions = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
last_predictions.drop('rui', inplace=True, axis=1)



sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo_items = sp.KNNBaseline(sim_options=sim_options)
algo_items.fit(trainset)


def get_item_recommendations(anime_title, anime_id=100000, k=10):
    if anime_id == 100000:
        anime_id = AnimesDF[AnimesDF['title'] == anime_title]['anime_id'].iloc[0]

    iid = algo_items.trainset.to_inner_iid(anime_id)
    neighbors = algo_items.get_neighbors(iid, k=k)
    raw_neighbors = (algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors)
    df = pd.DataFrame(raw_neighbors, columns=['Anime_ID'])
    df = pd.merge(df, AnimesDF, left_on='Anime_ID', right_on='anime_id', how='left')
    return df[['Anime_ID']]


def sortare(l, l_frec):
    for i in range(len(l_frec) - 1):
        for j in range(i + 1, len(l_frec) ):
            if(l_frec[i] < l_frec[j]):
                contor = l_frec[i]
                l_frec[i] = l_frec[j]
                l_frec[j] = contor
                contor = l[i]
                l[i] = l[j]
                l[j] = contor
    return l


def recommendation_system(anime):
    final = []
    final_frecv = []
    for a in anime:
        lista = get_item_recommendations(a.title, anime_id=a.anime_id, k=30)
        lista = lista['Anime_ID']
        for l in lista:
            if(len(final)==0):
                final.append(l)
                final_frecv.append(1)
            else:
                if(l in final):
                    poz = final.index(l)
                    final_frecv[poz] += 1
                else:
                    final.append(l)
                    final_frecv.append(1)
    return sortare(final, final_frecv)

