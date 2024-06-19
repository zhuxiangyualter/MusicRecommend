import pandas as pd
from django.contrib import messages
from django.http import HttpRequest
from surprise import SVD, KNNBasic
from surprise import Dataset, Reader, Prediction

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User
from music.models import UserProfile, Music

def build_df():
    data = []
    for user_profile in UserProfile.objects.all():
        for like_music in user_profile.likes.all():
            data.append([user_profile.user.id, like_music.pk, 1])
        for dislike_music in user_profile.dislikes.all():
            data.append([user_profile.user.id, dislike_music.pk, 0])
    return pd.DataFrame(data, columns=['userID', 'itemID', 'rating'])

def build_predictions(df: pd.DataFrame, user: User):
    userId = user.id
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return []

    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    subsets = df[['itemID']].drop_duplicates()
    testset = []
    for row in subsets.iterrows():
        testset.append([userId, row[1].values[0], 0])
    predictions = algo.test(testset, verbose=True)
    result_set = []

    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for item in predictions:
        prediction: Prediction = item
        if prediction.est > 0.70:
            music = Music.objects.get(pk=prediction.iid)
            if music in user_like:
                continue
            if music in user_dislike:
                continue
            result_set.append((music, prediction.est))

    if len(result_set) == 0:
        messages.error(current_request, '你听的歌太少了，多听点歌再来吧~')

    return result_set

def build_random_recommendations(user: User, num_recommendations: int = 20):
    user_profile = UserProfile.objects.get(user=user)
    user_like = user_profile.likes.all()
    user_dislike = user_profile.dislikes.all()

    all_music = Music.objects.exclude(pk__in=[music.pk for music in user_like]).exclude(pk__in=[music.pk for music in user_dislike])
    random_recommendations = all_music.order_by('?')[:num_recommendations]

    return list(random_recommendations)

def build_genre_predictions(user: User):
    predictions = []
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return predictions

    genre_subscribe = profile_obj.genre_subscribe.split(',')
    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for music in Music.objects.filter(genre_ids__in=genre_subscribe):
        if music in user_like:
            continue
        if music in user_dislike:
            continue
        predictions.append((music, None))

    return predictions

def build_language_predictions(user: User):
    predictions = []
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return predictions

    language_subscribe = profile_obj.language_subscribe.split(',')
    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for music in Music.objects.filter(language__in=language_subscribe):
        if music in user_like:
            continue
        if music in user_dislike:
            continue
        predictions.append((music, None))

    return predictions

def build_recommend(request: HttpRequest, user: User):
    global current_request
    current_request = request
    predictions = []
    predictions.extend(build_predictions(build_df(), user))
    predictions.extend(build_genre_predictions(user))
    predictions.extend(build_language_predictions(user))
    if len(predictions) == 0:
        predictions.extend(build_random_recommendations(user))
    return predictions[:20]


# if __name__ == '__main__':
#     # print(build_df())
#     # print(build_predictions(build_df(), User.objects.get(pk=4)))
#     # print(build_genre_predictions(User.objects.get(pk=2)))
#     # print(build_language_predictions(User.objects.get(pk=2)))
#     print(build_recommend(User.objects.get(pk=1)))
