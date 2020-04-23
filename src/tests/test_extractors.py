import pytest

from extractors import email_extractor


@pytest.mark.parametrize("text,email,expected", [
    ("ddd jsmith@apache.org ddd", "jsmith@apache.org", True),
    ("ddd jsmith@apache.org ddd x@example.com asdfk", "jsmith@apache.org", True),
    ("ddd jsmith@apache.org ddd x@example.com asdfk", "x@example.com", True),
    ("someone@216.109.118.76.", "someone@216.109.118.76", True),
    (".someone@yahoo.com", "someone@yahoo.com", True),
    ("'weirder-email@Here.and.there.com'", "weirder-email@Here.and.there.com", True),
    ("very.common@example.com", "very.common@example.com", True),
    ("other.email-with-dash@example.com", "other.email-with-dash@example.com", True),
    ("x@example.com", "x@example.com", True),
    ("email@localhost", "email@localhost", False),
    ("something@@somewhere.com", "something@@somewhere.com", False),
    ("jsmith@apache.c", "jsmith@apache.c", False),
    ("A@b@c@example.com", "A@b@c@example.com", False),
    ("asdf  asdfjj ofv lsdfk", "jsmith@apache.org", False)
])
class TestEmailExtraction:
    def test_email_extractor(self, text: str, email: str, expected: bool):
        assert any((email == result.group()) for result in email_extractor(text)) == expected
