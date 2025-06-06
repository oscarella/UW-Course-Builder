import re

def htmlfy_body(body):
    # Body is of bulleted list
    if re.search(r"<<\d+>>", body):
        retval = ""
        tlen = len(body)
        i = 0
        while i < tlen:
            # Found indent
            if body[i] == "<" and i < (tlen-2) and body[i+1] == "<":
                i += 2
                digits = ""
                # Find indent spacing
                while not (i >= tlen or (body[i] == ">" and i < (tlen-1) and body[i+1] == ">")):
                    digits += body[i]
                    i += 1
                i += 2
                text = ""
                # Populate text
                while i < tlen and not (body[i] == "<" and i < (tlen-2) and body[i+1] == "<"):
                    text += body[i]
                    i += 1
                digits.strip()
                text.strip()
                retval += "<p class=\"h6\" style=\"font-size: large; width: " + str((100 - 5 * (int(digits) - 1))) + "%; margin-left: " + str((5 * (int(digits) - 1))) + "%; text-align: left\">" + "&#x2022;" + text + "</p>"
            else:
                i += 1
        retval += "</br>"
        return retval
    else:
        return "<p class=\"h6\" style=\"font-size: large\">" + body + "</p> </br>"

def htmlfy(text):
    li = []
    retval = ""
    tlen = len(text)
    i = 0
    # li consists of [(heading1, body1), ...]
    while i < tlen:
        # Found heading
        if text[i] == "[" and i < (tlen-2) and text[i+1] == "[":
            i += 2
            heading = ""
            # Populate heading
            while not (i >= tlen or (text[i] == "]" and i < (tlen-1) and text[i+1] == "]")):
                heading += text[i]
                i += 1
            i += 2
            body = ""
            # Populate body
            while i < tlen and not (text[i] == "[" and i < (tlen-2) and text[i+1] == "["):
                body += text[i]
                i += 1
            heading.strip()
            body.strip()
            li.append((heading, body))
        else:
            i += 1
    # Create html code as return val
    for heading, body in li:
        retval += "<h4 style=\"color: #fcba03\">" + heading + "</h4>"
        retval += htmlfy_body(body)
    return retval