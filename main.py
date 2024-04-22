import json

import requests
from pyspark.sql import SparkSession


def evaluate(text: str, id: str) -> dict:
    """
    This one could also process list of text
    """
    url = "http://localhost:8982/content/topics-detection-with-custom-categories"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        "text": [text],
        "categories": ["positive", "negative"],
        "hypothesis_template": "The sentiment of this text is"
    })

    headers = {"Content-Type": "application/json"}

    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        data=data,
    )

    if response.status_code == 200:
        data = response.json()
        contents = data["contents"][0]
        return max(contents, key=lambda x: x["confidence"])["topic"], id
    else:
        return "error", id

def init_spark(cluster_mode: bool=False) -> SparkSession:
    if cluster_mode:    
        SparkSession.builder.master("local[*]").getOrCreate().stop()
        return SparkSession.\
            builder.\
            appName("demo").\
            remote("sc://172.17.0.1:7077").\
            getOrCreate()
    else:
        return SparkSession.builder.appName("demo").getOrCreate()

spark = init_spark()
sc = spark.sparkContext
df = spark.read.option("header", True).csv("samples/amazon_reviews_us_Baby_v1_00_sample.csv")
print(df.columns)

raw_reviews = df.select(["review_body", "review_id"]).collect()
reviews = [{"text": v["review_body"], "id": v["review_id"]} for v in raw_reviews]
print(reviews)

distData = sc.parallelize(reviews)
evalData = distData.map(lambda s: evaluate(**s))
print(evalData.collect())