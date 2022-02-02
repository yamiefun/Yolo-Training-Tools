import argparse
import os
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path", required=True)
    parser.add_argument("--classname", required=True)
    return parser.parse_args()


def parse_classname(path: str) -> list:
    cat_list = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            cat_list.append(line.split()[0])
    return cat_list


def main() -> None:
    args = parse_args()
    label_list = [
        os.path.join(args.folder_path, filename)
        for filename in os.listdir(args.folder_path)
        if filename[-4:] == ".txt"
    ]
    counter = defaultdict(int)
    for label_file in label_list:
        with open(label_file, "r") as f:
            lines = f.readlines()
        for line in lines:
            category = line.split()[0]
            counter[category] += 1
    keys = sorted(counter.keys())
    total_count = sum(counter.values())
    category_list = parse_classname(args.classname)
    print(f"Number of image: {len(label_list)}")
    for key in keys:
        print(f"Category: {category_list[int(key)]},"
              f" Number: {counter[key]}")
    print(f"Total: {total_count} bounding boxes.")


if __name__ == "__main__":
    main()
