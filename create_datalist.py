import os
import argparse
from random import shuffle


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path")
    return parser.parse_args()


def write_file(prefix: str, filename: str, image_list) -> None:
    with open(filename, 'w') as f:
        for image in image_list:
            image_name = os.path.join(prefix, image)
            f.write(f"{image_name}\n")


def main():
    args = parse_args()
    image_list = [filename for filename in os.listdir(args.folder_path)
                  if filename[-4:] != ".txt"]
    validation_count = int(len(image_list) * 0.1)
    print(f"Training set count: {len(image_list) - validation_count}")
    print(f"Validation set count: {validation_count}")
    shuffle(image_list)
    write_file(args.folder_path, 'valid.txt', image_list[:validation_count])
    write_file(args.folder_path, 'train.txt', image_list[validation_count:])


if __name__ == "__main__":
    main()
