import cerberus
import re
import html

comment_schema = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    },
    'comment': {
        'type': 'string'
    }
}

comments = []


def add_comment(email, comment):
    """Add a comment."""
    html_safe_comment = html.escape(comment)
    d = {'email': email, 'comment': html_safe_comment}
    v = cerberus.Validator(comment_schema)
    if v.validate(d):
        comments.append(d)
        return d
    else:
        return v.errors


def test_add_comment():
    value_regex = re.compile("^value does not match regex*")

    # Email - Happy path
    assert add_comment('ed@example.com', "What's up?") == {'email': 'ed@example.com', 'comment': "What&#x27;s up?"}
    assert add_comment('ed+eddy@example.com', "What's up?") == {'email': 'ed+eddy@example.com', 'comment': "What&#x27;s up?"}
    assert add_comment('ed+eddy@test.example.com', "What's up?") == {'email': 'ed+eddy@test.example.com', 'comment': "What&#x27;s up?"}
    # Email - sad/bad path
    assert value_regex.match(add_comment('ed@', "What's up?")['email'][0])
    assert value_regex.match(add_comment('@.com', "What's up?")['email'][0])
    assert value_regex.match(add_comment('ed@@example.com', "What's up?")['email'][0])
    assert add_comment('ed@example.com', '<script>alert("hi!")</script>') == {'email': 'ed@example.com', 'comment': '&lt;script&gt;alert(&quot;hi!&quot;)&lt;/script&gt;'}
