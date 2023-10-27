import responses
from gql import gql


@responses.activate(registry=responses.registries.OrderedRegistry)
def test_client_executes_simple_requests(test_url, api_client):
    ok_response = responses.post(test_url, status=200, body='{"data": {"ok": true}}')
    query = gql("query someQuery { ok }")
    result = api_client.execute_gql(query)
    assert result == {"ok": True}
    assert ok_response.call_count == 1


@responses.activate(registry=responses.registries.OrderedRegistry)
def test_client_retries_on_429(api_client, test_url):
    throttled_body = '{"errors": [{"message": "429 Too Many Requests"}]}'
    ok_body = '{"data": {"ok": true}}'

    resp1 = responses.post(test_url, status=429, body=throttled_body)
    resp2 = responses.post(test_url, status=429, body=throttled_body)
    resp3 = responses.post(test_url, status=429, body=throttled_body)
    resp4 = responses.post(test_url, status=200, body=ok_body)

    query = gql("query someQuery { ok }")
    result = api_client.execute_gql(query)
    assert result == {"ok": True}

    assert resp1.call_count == 1
    assert resp2.call_count == 1
    assert resp3.call_count == 1
    assert resp4.call_count == 1


@responses.activate(registry=responses.registries.OrderedRegistry)
def test_client_retries_on_500_errors(api_client, test_url):
    ok_body = '{"data": {"ok": true}}'

    resps = [responses.post(test_url, status=status) for status in [500, 502, 503, 504]]

    resps.append(responses.post(test_url, status=200, body=ok_body))

    query = gql("query someQuery { ok }")
    result = api_client.execute_gql(query)
    assert result == {"ok": True}
    assert all(resp.call_count == 1 for resp in resps)
