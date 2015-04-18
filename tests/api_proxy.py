def request_callback(request, uri, headers):
    # parse_xml() extracts important data from request
    data = parse_xml(request.body)
    # response based on that data
    if data.something_important:
        return (200, headers, "relevant data")
    else:
        return (400, headers, "panic mode!")
