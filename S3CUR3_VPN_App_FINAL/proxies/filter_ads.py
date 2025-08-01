# filter_ads.py

from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    if "ads" in flow.request.pretty_url or "doubleclick" in flow.request.pretty_url:
        flow.response = http.HTTPResponse.make(
            204,  # No Content
            b"",
            {"Content-Type": "text/plain"}
        )
