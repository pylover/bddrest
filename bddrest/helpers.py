from urllib.parse import parse_qs


def normalize_query_string(query):
    if not query:
        return None
    return {
        k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()
    } if isinstance(query, str) else query

