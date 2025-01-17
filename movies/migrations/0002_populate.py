import os

import numpy as np
import pandas as pd
from babel import Locale
from django.db import migrations
from tqdm import tqdm


def use_none(data):
    return data.replace({np.nan: None})


def convert_to_list(data):
    json_columns = ["genres", "production_companies", "credits", "keywords", "recommendations"]
    data[json_columns] = data[json_columns].applymap(lambda x: x.split("-") if x else None)
    return data


def convert_image_path_to_url(data):
    image_columns = ["poster_path", "backdrop_path"]
    data[image_columns] = data[image_columns].applymap(lambda x: f"https://image.tmdb.org/t/p/w500{x}" if x else None)
    return data


def remove_duplicates(data):
    return data.drop_duplicates("id")


def remove_movies_without_title(data):
    return data.dropna(subset=["title"])


def replace_languages(data):
    data["original_language"] = data["original_language"].replace("cn", "zh")
    return data


def read_data():
    dir_path = "temp/data"
    file_path = os.path.join(dir_path, "movies_dataset.csv")
    os.makedirs(dir_path, exist_ok=True)

    if os.path.exists(file_path):
        print("Reading data from local file")
        data = pd.read_csv(file_path)
    else:
        print("Reading data from remote file, it may take a while...")
        data = pd.read_csv("hf://datasets/wykonos/movies/movies_dataset.csv")
        print("Reading complete. Saving data to local file")
        data.to_csv(file_path, index=False)
    return data.iloc[:1000]


def create_entity(model, data, field):
    instances = data[field].explode().dropna().unique()
    total = instances.shape[0]

    print(f"Populating {total} {model._meta.verbose_name_plural}...")
    with tqdm(total=total) as t:
        for instance in instances:
            model.objects.get_or_create(name=instance)
            t.update(1)


def create_genres(Genre, data):
    create_entity(Genre, data, "genres")


def create_languages(Language, data):
    codes = data["original_language"].dropna().unique()
    instances = pd.DataFrame(codes, columns=["code"])
    instances["name"] = instances["code"].apply(lambda x: Locale("en").languages[x])
    total = instances.shape[0]

    print(f"Populating {total} {Language._meta.verbose_name_plural}...")
    with tqdm(total=total) as t:
        for _, instance in instances.iterrows():
            Language.objects.get_or_create(code=instance["code"], name=instance["name"])
            t.update(1)


def create_companies(Company, data):
    create_entity(Company, data, "production_companies")


def create_contributors(Contributor, data):
    create_entity(Contributor, data, "credits")


def create_keywords(Keyword, data):
    create_entity(Keyword, data, "keywords")


def create_movies(Movie, Genre, Language, Company, Contributor, Keyword, data):
    total = data.shape[0]

    print(f"Populating {total} movies...")
    with tqdm(total=total) as t:
        for _, row in data.iterrows():
            genres = row.pop("genres") or []
            production_companies = row.pop("production_companies") or []
            credits = row.pop("credits") or []
            keywords = row.pop("keywords") or []
            recommendations = row.pop("recommendations") or []

            row["original_language"] = Language.objects.filter(code=row["original_language"]).first()

            movie = Movie.objects.create(**row.to_dict())

            movie.genres.set(Genre.objects.filter(name__in=genres))
            movie.production_companies.set(Company.objects.filter(name__in=production_companies))
            movie.credits.set(Contributor.objects.filter(name__in=credits))
            movie.keywords.set(Keyword.objects.filter(name__in=keywords))
            movie.recommendations.set(Movie.objects.filter(id__in=recommendations))
            t.update(1)


def populate(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    Genre = apps.get_model("movies", "Genre")
    Language = apps.get_model("movies", "Language")
    Company = apps.get_model("movies", "Company")
    Contributor = apps.get_model("movies", "Contributor")
    Keyword = apps.get_model("movies", "Keyword")

    data = read_data()
    data = use_none(data)
    data = convert_to_list(data)
    data = convert_image_path_to_url(data)
    data = remove_duplicates(data)
    data = remove_movies_without_title(data)
    data = replace_languages(data)

    create_genres(Genre, data)
    create_languages(Language, data)
    create_companies(Company, data)
    create_contributors(Contributor, data)
    create_keywords(Keyword, data)
    create_movies(Movie, Genre, Language, Company, Contributor, Keyword, data)


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate, reverse_code=migrations.RunPython.noop),
    ]
