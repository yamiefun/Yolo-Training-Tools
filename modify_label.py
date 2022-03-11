import argparse
import os

MAPPING = {'0': '0',
           '1': '1',
           '2': '2',
           '3': '3',
           '4': '4',
           '5': '5'}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path")
    return parser.parse_args()


def check_valid_bbox(line):
    info = line.split()
    if len(info) < 5:
        return False
    for idx in range(1, 5):
        if float(info[idx]) == 0:
            return False
    return True


def main() -> None:
    args = parse_args()
    for filename in os.listdir(args.folder_path):
        if filename[-4:] != ".txt":
            continue
        label_file = os.path.join(args.folder_path, filename)
        with open(label_file, "r") as f:
            lines = f.readlines()
        with open(label_file, "w") as f:
            for line in lines:
                if check_valid_bbox(line):
                    newline = MAPPING[line[0]] + line[1:]
                    f.write(newline)


if __name__ == "__main__":
    main()
