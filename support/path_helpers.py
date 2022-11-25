def convert_unc(path: str) -> str:
    if path.startswith("file://"):
        return path.replace("file://", "")


def get_unique_filename(path: str) -> str:
    ...


def make_resource_path(path: str):
    return path


def make_image_path(filename: str) -> str:
    return f"resources/images/{filename}"


def make_icon_path(filename: str) -> str:
    return f"resources/icons/{filename}"


def make_recipe_path(filename: str) -> str:
    return f"resources/recipes/{filename}"


def endswith_any(path: str, suffixes: list) -> bool:
    for suffix in suffixes:
        if path.endswith(suffix):
            return True
    return False
