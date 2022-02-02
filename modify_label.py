import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder_path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    label_list = [
        os.path.join(args.folder_path, filename)
        for filename in os.listdir(args.folder_path)
        if filename[-4:] == ".txt"
    ]
    for label_file in label_list:
        with open(label_file, "r") as f:
            lines = f.readlines()
        with open(label_file, "w") as f:
            for line in lines:
                newline = '1' if line[0] == '0' else '0'
                newline += line[1:]
                f.write(newline)


if __name__ == "__main__":
    main()
