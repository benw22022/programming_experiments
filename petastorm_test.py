import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField

import awkward as ak
import glob
import uproot

variables = [
"TauTracks.nInnermostPixelHits",
"TauTracks.nPixelHits",
"TauTracks.nSCTHits",
"TauTracks.chargedScoreRNN",
"TauTracks.isolationScoreRNN",
"TauTracks.conversionScoreRNN",
"TauTracks.pt",
"TauTracks.dphiECal",
"TauTracks.detaECal",
"TauTracks.jetpt",
"TauTracks.d0TJVA",
"TauTracks.d0SigTJVA",
"TauTracks.z0sinthetaTJVA",
"TauTracks.z0sinthetaSigTJVA"]

# The schema defines how the dataset schema looks like
schema = [UnischemaField(feature, np.float32, (None, 3), NdarrayCodec(), False) for feature in variables]
HelloWorldSchema = Unischema('TauTracksSchema', schema)


def row_generator(x, data):

    print(f"{x} / {len(data)}")
    features_dict = {}

    for feature in variables:
        arr = [0, 0, 0]
        for i in range(3):
            if i > len(data[x][feature]):
                break
            arr[i] = data[x][feature]

        features_dict[feature] = arr

    return features_dict

def generate_petastorm_dataset(output_url='file:///tmp/hello_world_dataset'):
    rowgroup_size_mb = 256

    spark = SparkSession.builder.config('spark.driver.memory', '2g').master('local[2]').getOrCreate()
    sc = spark.sparkContext

    data = uproot.lazy(glob.glob("../NTuples/*Gammatautau*/*.root")[0])

    # Wrap dataset materialization portion. Will take care of setting up spark environment variables as
    # well as save petastorm specific metadata
    rows_count = 10
    with materialize_dataset(spark, output_url, HelloWorldSchema, rowgroup_size_mb):

        rows_rdd = sc.parallelize(range(rows_count))\
            .map(lambda x: row_generator(x, data))\
            .map(lambda x: dict_to_spark_row(HelloWorldSchema, x))

        spark.createDataFrame(rows_rdd, HelloWorldSchema.as_spark_schema()) \
            .coalesce(10) \
            .write \
            .mode('overwrite') \
            .parquet(output_url)

if __name__ == "__main__":
    # print(row_generator(0, data = uproot.lazy(glob.glob("../NTuples/*Gammatautau*/*.root")[0])))
    generate_petastorm_dataset(output_url='file:test_dataset')