def get_route_base_from_path(path: str) -> str:
    try:
        return path.split("/")[3]
    except IndexError:
        return ""
