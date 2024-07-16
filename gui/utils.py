import yaml
import os


def yaml_file_to_dict(translations_dir: os.PathLike, lang: str, level: str) -> dict:
    with open(f"{translations_dir}/en_{lang}.yaml", "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader).get(level, None)
        assert isinstance(content, dict)
        return content
