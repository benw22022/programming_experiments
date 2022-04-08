from matplotlib.pyplot import arrow
from matplotlib.style import library
import uproot
import awkward as ak
import ray
from variables import variable_handler
import tensorflow_io.arrow as arrow_io
import tensorflow as tf

if __name__ == "__main__":


    for i, batch in enumerate(uproot.iterate("TestFile.root", library="ak", filter_name=variable_handler.list(), step_size=32)):
        
        # arrow_array = ak.to_arrow(batch)

        # print(arrow_array)

        # ds = arrow_io.ArrowDataset(arrow_array, columns=variable_handler.list(), output_types=[tf.float32 for _ in variable_handler.list()])


        # ds = ray.data.from_items(arrow_array).write_parquet(f"data/test_data_{i}.parquet")

        # print(ds)

        break