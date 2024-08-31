MAX_LITERAL_LEN = 40


def loststr(s, maxlen=MAX_LITERAL_LEN):
    if len(s) > maxlen:
        return f'{s[:maxlen // 3]}...{s[-(maxlen // 3):]}'

    return s
