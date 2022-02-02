# YOLO Training Tools

## Create Training and Validation List

### Purpose

If you train model without a validation set, it's hard for you to estimate the training result, and may lead to overfitting problem.
Hence, after downloading the whole dataset, we need to split it into two subset: training and validating the model.

### Usage

1. Put all images and labels into a folder.
2. Run `create_datalist.py` as follow:

    ```terminal
    python3 create_datalist.py --folder_path <dataset folder>
    ```

3. This code will automatically generate `train.txt` and `valid.txt` for training process. By default, the size of validation set will be 10% of total number images. In other words, training set will be 90% of the total size.

4. Put the path of `train.txt` and `valid.txt` into the training config file of Yolo(e.g., `obj.data`), and you can start training your model.

## Merge Different Project on Label-Studio (*NOT FINISH YET*)

### Purpose

If you want to merge two project on Label-Studio with same categories, sometimes it will generate the classname file in different order. You could use `modify_label.py` to fix it.

## Count Number of Bounding Box in Dataset

### Purpose

Count the number of bounding boxes for each categories in the dataset.

### Usage

```terminal
$ python3 bbox_counter.py \
    --folder_path <dataset folder> \
    --classname <classname file>
# example output:
    Category: adult_female, Number: 3296
    Category: adult_male, Number: 7750
    Total: 11046 bounding boxes.
```

## Draw Bounding Boxes on Dataset (*NOT FINISH YET*)

### Purpose

To easily visualize the training result, you could use `darknet_demo_images.py` to draw bounding boxes on a list of images.

### Usage

+ List paths to each image in a `txt` file. For example, you could directly regard `valid.txt` as an image list.

+ Copy `darknet_demo_images.py` to `darknet` folder.

    ```terminal
    cp tool/darknet_demo_images.py .
    ```

+ Execute

    ```terminal
    python3 darknet_demo_images.py \
        --input <image list> \
        --weights <weights file> \
        --ext_output \
        --config_file <config file> \
        --data_file <data file> \
        --dont_show --write_image \
        --thresh <confidence thresh>

    # For example,
    python3 darknet_demo_images.py \
        --input valid.txt \
        --weights backup/yolov4/yolo-obj_final.weights \
        --ext_output \
        --config_file cfg/yolo-obj.cfg \
        --data_file data/obj.data \
        --dont_show --write_image \
        --thresh 0.7
    ```
