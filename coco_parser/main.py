from pycocotools.coco import COCO
import requests
import os
import argparse
import sys
import json

COCO_LABEL_FILE = "coco_labels.txt"
SUPPORTED_MODE = {"union", "intersection"}
SUPPORTED_NUM = {"min", "max"}


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help="Path to config file.",
                        default="config.json")
    config_file = open(parser.parse_args().config, 'r')
    config = json.loads(config_file.read())
    config_file.close()
    return config


def make_dirs_if_not_exist(args: dict) -> None:
    image_out = args["image_output_folder"]
    label_out = args["label_output_folder"]
    if not os.path.isdir(image_out):
        try:
            os.makedirs(image_out, exist_ok=True)
        except Exception:
            print(Exception)
    if not os.path.isdir(label_out):
        try:
            os.makedirs(label_out, exist_ok=True)
        except Exception:
            print(Exception)


class COCOParser:
    def __init__(self, args: dict):
        self.coco = COCO(args['coco_annotation'])
        self.coco_label = self._parse_label_file(COCO_LABEL_FILE)
        self.target = self._parse_label_file(args['target_category'])
        self._check_target_valid(self.target)
        self.image_save_path = args['image_output_folder']
        self.label_save_path = args['label_output_folder']
        self.download_mode = args['download_mode']
        self.download_num = args['download_num']

    def _create_obj_name_file(self, target: list[str]) -> None:
        """ Create `obj.names` for yolov4 training.

            Args:
                target (list[str]): All categories.

            Returns:
                None
        """
        with open("obj.names", "w") as f:
            for category in target:
                f.write(category+'\n')

    def _parse_label_file(self, label_file: str) -> set:
        """ Parse labels.

            Args:
                label_file (str): Path to label file.

            Returns:
                (set): All categories in label file.
        """
        try:
            labels = open(label_file, 'r')
        except OSError:
            print(f"Cannot open label file: {label_file}.")
            sys.exit()
        categories = labels.readlines()
        return {category.rstrip('\n')
                for category in categories if category.rstrip('\n')}

    def _check_target_valid(self, target: set) -> None:
        """ Check all categories in target is valid.

            Args:
                target (set): All targets.

            Returns:
                None
        """
        for category in target:
            if not self.coco.getCatIds(catNms=[category]):
                raise ValueError(f"Category '{category}' is not included in "
                                 f"COCO labels.")

    def _instance_transformation(
            self, target_map: dict, inst: object, image: object):
        """ Transform coco instance labels to yolo format and custom id.
        """
        return (f"{target_map[inst['category_id']]} "
                f"{(inst['bbox'][0]+inst['bbox'][2]/2)/image['width']} "
                f"{(inst['bbox'][1]+inst['bbox'][3]/2)/image['height']} "
                f"{inst['bbox'][2]/image['width']} "
                f"{inst['bbox'][3]/image['height']}\n")

    def _get_image_id(self,
                      cat_ids: list[int], mode: str, num: str) -> list[int]:
        """ Get image ids by specific category ids and mode.

            Supported mode: `union` and `intersection`.
            + For union, downloaded images will contain at least one target
                categories.
            + For intersection, downloaded images will contain all target
                categories.

            Args:
                cat_ids (list[int]): List of category ids.
                mode (str): Download mode.

            Retunrs:
                (list[int]): List of image ids.
        """
        if mode not in SUPPORTED_MODE:
            raise ValueError(f"Download mode '{mode}' is not supported.")
        if num not in SUPPORTED_NUM:
            raise ValueError(f"Download num '{num}' is not supported.")

        print(f"Download mode: '{mode}', download num: '{num}'")
        if mode == 'union':
            image_ids, download_num = [], None
            if num == 'min':
                download_num = min(len((self.coco.getImgIds(catIds=cat_id)))
                                   for cat_id in cat_ids)
                print(f"Download num per category: {download_num}")
            for cat_id in cat_ids:
                image_ids.extend(
                    (self.coco.getImgIds(catIds=cat_id))[:download_num])
            return image_ids
        elif mode == 'intersection':
            return self.coco.getImgIds(catIds=cat_id)

    def download(self):
        """ Download and parse image from COCO dataset with target categories.
        """

        target = list(self.target)
        self._create_obj_name_file(target)
        # mapping between coco cat id and custom cat id
        target_map = {}
        for idx, category in enumerate(target):
            coco_cat_id = self.coco.getCatIds(catNms=[category])[0]
            target_map[coco_cat_id] = idx

        # get all coco catId
        cat_ids = self.coco.getCatIds(catNms=target)

        # get all image id contain the target category
        image_ids = self._get_image_id(cat_ids,
                                       mode=self.download_mode,
                                       num=self.download_num)

        total_num, count = len(image_ids), 0
        images = self.coco.loadImgs(image_ids)
        print(f"Total image count: {total_num}")
        for image in images:
            # download image
            image_data = requests.get(image['coco_url']).content

            # save image
            save_path = \
                f"{os.path.join(self.image_save_path, image['file_name'])}"
            with open(save_path, "wb") as handler:
                handler.write(image_data)

            # get annotation
            annotation_ids = self.coco.getAnnIds(imgIds=image['id'])
            annotations = self.coco.loadAnns(annotation_ids)

            # create yolo format label file
            label_file_name = \
                f"{self.label_save_path}/{image['file_name'][:-4]}.txt"

            with open(label_file_name, 'w') as f:
                for instance in annotations:
                    if instance['category_id'] not in target_map:
                        continue
                    line = self._instance_transformation(
                        target_map, instance, image)
                    f.write(line)

            print("finish images id ", image['id'])
            print(f"Progress: {count*100/total_num:.2f}% "
                  f"({count}/{total_num})")
            count += 1


def main():
    args = arg_parse()
    make_dirs_if_not_exist(args)
    coco_parser = COCOParser(args)
    coco_parser.download()


if __name__ == "__main__":
    main()
