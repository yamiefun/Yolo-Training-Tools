# COCO Yolo Parser

This tool can help you to download specific categories in COCO dataset and convert them into yolo's label format.

## Usage

### Environment and Setting
1. Create [Conda](https://docs.conda.io/en/latest/) environment. The recommended python version will be 3.9. After creating the environment, get into it.

    ```bash
    conda create --name <environment name> python=3.9
    conda activate <environment name>
    # ex:
    conda create --name coco2yolo python=3.9
    conda activate coco2yolo
    ```

2. Install requirements with the given `requirements.txt` file.

    ```bash
    pip3 install -r requirements.txt
    ```

3. Download [COCO annotations](https://cocodataset.org/#download) and place it in this repository. For example, [2014 Train/Val annotations [241MB]](http://images.cocodataset.org/annotations/annotations_trainval2014.zip). Please note that you don't need to download images, only annotations are needed.

4. Modify `config.json`. There are 6 fields in the config file. Here's the explanation for each of them.
    + `coco_annotation`: Path to the annotation file that is downloaded in the previous step.
    + `image_output_folder`: Folder name or path to store downloaded images.
    + `label_output_folder`: Folder name or path to store downloaded labels.
    + `download_mode`: Mode to download. Current supported modes: `union`, `intersection`.
        + `union`: Images will be downloaded if there's at least one object that is the category that you want to download.
        + `Intersection`: Images will be downloaded only if all target categories appear in those images.
    + `download_num`: This parameter only works if you use `union` in `download_mode`. You can use `min` or `max` in this field.
        + `min`: The downloaded image in each target category will be the same, equals to the category that has the least number of images.
        + `max`: All image with target categories will be downloaded.
    + `target_category`: Path to target categories list. The target list should be a text file, including one category in each line.  For example,
        ```
        car
        person
        cat
        ...
        ```
        If some categories are not included in COCO dataset, this program will ask you to modify the target categories file.

### Execute
+ After `config.json` is set properly, you can simply run the program with

    ```bash
    python3 main.py --config <config file>
    # ex:
    python3 main.py --config config.txt
    ```
+ Folders will be created to store image and labels.
+ A file called `obj.names` will be created. All target categories will be store in it with different order with your original target categories file. All label files' label id is mapped with `obj.names`, hence, you can directly use `obj.names` when you train yolo.
## Tips
1. If you have lots of categories want to download, you should use `union` with `min` to make the number of images (labels) between different categories similar.

2. If you have a custom dataset needs to merge with COCO data, you can futher use [this tool](https://github.com/yamiefun/Yolo-Training-Tools#merge-different-project-on-label-studio-not-finish-yet) to modify label id.