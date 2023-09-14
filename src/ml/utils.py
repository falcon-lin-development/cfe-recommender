from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.core.files.base import File
from django.conf import settings

from ratings.models import Rating
from exports import storages as export_storages

from surprise import Dataset, accuracy, Reader, SVD
from surprise.model_selection import cross_validate

import pickle
import tempfile


def export_ratings_dataset():
    ctype = ContentType.objects.get(app_label="movies", model="movie")
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(
        userId=F("user_id"), movieId=F("object_id"), rating=F("value"),
    )
    return qs.values("userId", "movieId", "rating") # [{}]


def get_data_loader(dataset, columns=['userId', "movieId", "rating"]):
    import pandas as pd
    df = pd.DataFrame(dataset) 
    df['rating'].dropna(inplace=True)
    max_rating = df['rating'].max()
    min_rating = df['rating'].min()
    reader = Reader(rating_scale=(min_rating, max_rating))

    return Dataset.load_from_df(df[columns], reader)

def get_model_acc(trainset, model, use_rmse=True):
    testset = trainset.build_testset()
    predictions = model.test(testset)
    # RMSE should be low as we are biased
    if not use_rmse:
        acc =  accuracy.mae(predictions, verbose=True)
    else:
        acc = accuracy.rmse(predictions, verbose=True)
    return acc

def train_surprise_model(n_epochs=20, verbose=True,):
    dataset = export_ratings_dataset()
    loaded_data = get_data_loader(dataset)
    model = SVD(n_epochs=n_epochs, verbose=verbose)
    cv_results = cross_validate(
        model, 
        loaded_data, 
        measures=['RMSE', 'MAE'], 
        cv=5, 
        verbose=True
    )
    trainset = loaded_data.build_full_trainset()
    model.fit(trainset)
    acc = get_model_acc(trainset, model, use_rmse=True)
    acc_label = int(100 * acc)
    model_name = f"model-{acc_label}"
    export_model(model, model_name=model_name, model_type="surprise", model_ext="pkl", verbose=True)

def export_model(
        model, model_name="model", 
        model_type="surprise", model_ext="pkl", 
        verbose=True             
    ):
    with tempfile.NamedTemporaryFile(mode="rb+") as temp_f:
        model_data = {"model": model}
        pickle.dump(model_data, temp_f)
        path = f"ml/models/{model_type}/{model_name}.{model_ext}"
        path_latest = f"ml/models/{model_type}/latest.{model_ext}"
        if verbose:
            print(f"Saving model to {path} and {path_latest}")
        export_storages.save(path, File(temp_f))
        export_storages.save(path_latest, File(temp_f), overwrite=True)

def load_model(model_type="surprise", model_ext="pkl"):
    path_latest = settings.MEDIA_ROOT / f"ml/models/{model_type}/latest.{model_ext}"

    model = None
    if path_latest.exists():
        with open(path_latest, "rb") as f:
            model_data = pickle.load(f)
            model = model_data.get("model")
    return model