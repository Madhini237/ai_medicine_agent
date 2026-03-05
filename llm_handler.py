def understand_reply(text):

    text = text.lower()

    taken_words = ["took", "taken", "done", "yes"]
    delay_words = ["later", "wait"]
    miss_words = ["forgot", "not taken"]

    for w in taken_words:
        if w in text:
            return "MEDICINE_TAKEN"

    for w in delay_words:
        if w in text:
            return "DELAYED"

    for w in miss_words:
        if w in text:
            return "MISSED"

    return "UNKNOWN"