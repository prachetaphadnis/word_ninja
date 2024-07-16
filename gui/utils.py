import yaml
import os


def yaml_file_to_dict(input_path: os.PathLike) -> dict:
    with open(input_path, "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        assert isinstance(content, dict)
        return content
