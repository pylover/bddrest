from urllib.parse import parse_qs


def normalize_headers(headers):
    if not headers:
        return None

    headers = [h.split(':', 1) if isinstance(h, str) else h for h in headers]
    headers = [(k.strip(), v.strip()) for k, v in headers]
    return headers


def normalize_query_string(query):
    if not query:
        return None
    return {
        k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()
    } if isinstance(query, str) else query


class Headers(list):
    pass

