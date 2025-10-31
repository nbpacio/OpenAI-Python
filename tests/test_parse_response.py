import types

from OpenAI_Python import parse_response


def test_parse_response_output_text():
    class Resp:
        output_text = "hello from output_text"

    assert parse_response(Resp()) == "hello from output_text"


def test_parse_response_output_list_of_dicts():
    resp = types.SimpleNamespace()
    resp.output = [
        {"content": [{"text": "part1"}, {"text": "part2"}]},
        {"text": "block-level"},
    ]

    got = parse_response(resp)
    assert "part1" in got
    assert "part2" in got
    assert "block-level" in got


def test_parse_response_object_blocks_with_attrs():
    class Block:
        def __init__(self, text):
            self.text = text

    resp = types.SimpleNamespace()
    resp.output = [Block("attribute text")] 
    assert parse_response(resp) == "attribute text"


def test_parse_response_to_dict_fallback():
    class Resp:
        def to_dict(self):
            return {"a": 1}

    got = parse_response(Resp())
    # to_dict result is stringified
    assert "{'a': 1}" in got or '"a": 1' in got
