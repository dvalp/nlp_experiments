import pytest

from src.utilities.count_substrings import count_unique_substrings

testdata = [
    ("dbdbdbacdbcdab", 88),
    ("dccadcadbcada", 76),
    ("bdcaddcda", 40),
    ("ac", 4),
    ("cc", 3),
    ("cdbdccbdaada", 69),
    ("bdaccabbcac", 58),
    (
        "cdaaddddbaddcdbcdcdbaaaaadbbbbcdaabcabbcdcddbbbccdbccbbcccacdbdbddbbbcddabbdbaabcbdbdbccdbadcadabaabbcbabdbdb"
        "abddcabccdcbacdbadbbddcbcdcaaabbacbadbcadcdcccccdbbacdcadbdccdbaccbbcdddacccadddcacbcddddadcbaddabdabacccdbda"
        "cbbdadcabccdcaaaacabcdddabdacabcaaadadbaabddccabdaacdabbadacbdbbdadcdbadaadacadaacacdcacdbcbdcaadcccaabcadcbb"
        "abdbaddadacbccbaadadbcccbdccbdbbacbadaaadadadabdacaddadbbbcbcbccadcdaaccdcdbbccbdcdcabbacacbaaccdbbdbccdbbcca"
        "bdacbdaddaccbddbcadaccacdaabddcbcddcadababdaccadddadbccbdbbbddabacbaccbdcdbadacbcdbddccbcabddddaaadabacbdaadb"
        "bdcaacadcbdcdacddacddadadddbbbdaadaabdbbbcddbbbcaacadcbacdcdcacaaaacadbbccbcacdbdabacbbcdbdbabcaccbbabddcbcab"
        "bbdcbdddadbddbddbdaddacbbbbcdadbdbadaabcbdcbdcabacbcdbbaadbcacddcadbaaababcddbcdcccadaacbcccabaccddadbaabacbc"
        "aacacaccdcaccdcbdadcddcadcdccaabdcbbcaadcbadaaccaadadaabdadccadadadcdbccbcdabaddadbdccacdaaaadbadacdbcaccbbca"
        "cdccccccdbbdacbbcbdbcbacdadbddddaaddaccadbbddbbbddccccdbacdbbadbdadaabddbacddbbbdcbabddbbcbdbcbdaaadcdacaabbb"
        "bddcbcbbbabacbabbcbbcdbddcaabaacacbcdddcccaadcdbdaddbcdaadabaaabcddbdcccaaadaaaabcdcbadacabdadadbcdcdbdaacacb"
        "abdaadbbbdaadacbdcdbababcaababacababcccacaabdabcaabdadacdbabcdababcdaaaaaabaacbbcbbcabacdadbaabbacbcadabadaba"
        "dbadcacdccbaaccaacbadcbccddbabbbacbabaadadbdadbdcbdccadcccbaccaccadbdbdabadcaabadadadcccdddcabcdaadddccdccddd"
        "ddbcdcbcdcacbcdccccdccaccddbdcacdaddbbabaaabddacbbdcadcabbdcccbbdbadadccaadbacccbdabdbcdbbaccbbccddacbdcbaada"
        "bdaccbccdcdcacabaaadabadcbdbdbbbddaccaadddbaadbcdabdaacbdbdcbbabcddbabaddcdccbdcbccbcbdddcadaaaaddbcbccdbbccd"
        "ccbdcdcccaabccccccdbbacadccacbdadbdcdacadcddadbddcccbdbaaadddbbabdabdbdcbcccbdbcbcbbdbdacbdcccabadaabaaaacacc"
        "aabdadcdddbcdbdcadabcabbbbbbbddcbaacbdcbbdbcadcdaacdadbadcbcbabdbcdbbadcbccbcacbdddddbacbbbbbbddddaccdbbdbbad"
        "cdbabbbbadddacdabdacacdcdbdcddbadddbbcdcaddddcdcdbbdcdbdcaccacbadabdcaadddadbabbcddbcaddddbbddacdcbccdccbcbaa"
        "bdadcaadcaabbaacbacbdccbaabbaacacdcddcacadbdbbaacccdcccbdcdddbacdcbbabdbdcbbbddbbcdddddbbadbbbabbdcacdbddacad"
        "bbacbcdabaacbbddbabbabaddbdaddbccbacabaadcbcccccbcaabdacabcbaacacacbaadbadccbaaacbbbdbbdcdacacbccbbcadaddabac"
        "babacaabacababadacadbbabcdbbcccdbdbdcbaabbcdadcaadabbbacbadaaacaadbdbdbacbcbccadcb",
        2308586),
    (
        "caccadabadadbdccacddcbcbbdbacddbcaacccbbaadacdabddbaabadcbbcbcddcbcddcbdddbbabaacbbaddadcadaaddcddccadcddcbcd"
        "bbaadcddadbdcbabbddbdbbbdaddcdacbcdbadcaccdccdddbcccabbaccdcabaadbcbbbdadbbcadaabaacdadddcdcbddddccabbcbccabd"
        "abccdcddccbadcbbdcdcdbcbbabdbbdabdcddabaaadcbddaabadabcaabadbcbcacdaabdbcadadddbbbadaccdcdacabcdbaadabdccdbcc"
        "bcbdacddabdacbdbdcadadbdbadddccdadbabcdbcaddabccdabbadacbaadcdcbbcdbbadddcaacaaabbcbcccbbaddcbcabaabcaccdbdca"
        "bdacaabdabadbaacbbbbabdbadbcdcbdaddddcbacbcadaaddccbbadcbbadddbbcacddcdccadcdddddbcdbdaabaacbaccdcbbdadadbcab"
        "adabbddcdcabccccbaddcaaaabdbdabcdbacccbbabdcbbbaaadbababbddcaadcaccaabdbcacbbccdabbdcdacaacddaaaadbaacaaababd"
        "bddbaddaaadaadaddbbccadbcacdaacbddcddabcddddbcdbbacbdcbdabcddacccdbdaaddccabaddcdbddaacdbbbcbdccccbccacbdacbc"
        "ddcadbdabbbcdccbbdabdadadacbcaacdccabbaaadadabccaadcddbbdcdbacbcdbbadaddccacabaabadcdcacdabdbacbccdcdcdddacdb"
        "dbcbadbbadabdbcbacdccacdcdcadbabccacaddcabcddcaaaddaacabbaadaaabdddcbdccddaabdccbabdbbbcbacbdbaddccdbabbdcdbc"
        "cbaaadcbbcabdbbbbcadacbbbdabdcddadccacbdbcdbcaccabdccabaacacbadcabbadacaaddcbcbdaadbbcacbaddccbaacbddcccdaccd"
        "bbbccccbcaadcadddddbbdcccadabdaddcacaccdadccacbaddbbbcccccddcadaaaacccbcaccbaaaacabcbcdcbddbaacbacbdddaabcddd"
        "dbacdbbcbcdcdbcabccaabcbbddcddacdcddcbdddbaaacdcdbbbdcbddddbcbdbdcdddccbaabbdcbbccaaaaaabdbbdbaaccbcaddcbbabb"
        "dcddccbbababcbacbbcbadaaddcbcadbcacdddccccacbacacabbddbacbbcccababddcdbbadbacbbbacddbdabdcaddaabdccaadcabdacc"
        "accaabadadccaddbabdacdbcabbaddadbbddbadacccaaaabacacabddcaaacbdddabbabbaddccddadbaaaacbccbadcbcbdadbdacacabdb"
        "cbcbccbddacdbbacaaabccbbaaabacbbbdabacadadbdabcadcaaccaadcabcddbdacbabbbacdbbccacaacabccaadacacbcaaccbdbdbbdb"
        "cdbdcadcbbabbbadcdaacdbcbbccacaababdbbabdbacccdaccbdaabcabaaadbddacadcdcdbaadabccbbddbdcdaddbcdbbacabdbddbadd"
        "cdcdadbcdcaaccdbdaadccdcccbcdcacdacdbbadabbbdbbaacabacddcbbcaabddbdadabbbaccbccdabbcacacbdcccbbadaabbdccbdcbc"
        "babdbcbadbacacbcdcbdddacddbbcbcbbabdbacdcbcbbbbcdcacbdccccbcbccbcdadcdbddbdcacdbbbcdddacbbddadbdabbbcddcbdada"
        "bccdcacacaacccbcaccdcabcabdbbcbdbacbaaddbdbccbcacaadcbcbdb",
        2031740),
    (
        "ccdccadbdbcabcbdacaabdbdbcbadaccbbdbcddacdabaaaccbdbaacaabbaccabccaadaccbccadacddcddbbbcdbcbaddcabdadcdddaacd"
        "bdabbacbcccbccadacbcbcdddbccabddcaccabcdabdbbcbaabcbbacacacabdbcbccadccbabaadcabcabadaababbcdadadaddadcbcbbba"
        "dadcdcadcacbcdaddddcdccbcbdbabcdadabdcdabaaabbaadbabcbdbbdbbdbdacddcbdacdddadcbddacddccdbadaadcbccdcbbcacdcab"
        "dacbbcbabbaddacdcacdccbcbbddadbcbbcdcccbdcbbcdbbcddbcaddddaabddcdddccbacdddabbaccccdcabdadaddadbbabddbbcccdcc"
        "ababbbdbaccabbddbdbbddcabbbdcacbbdadbcaddabddcddcdcddacbbaabdcbaddcabcadbccdabbcadbcacdddcaccbdccbdcaadabdabc"
        "ccbaacccbacacbbbdcbcaabbadcabcbadacccdacdccdccaacdcbdccdcdacdadcddbbdadadabaacdcadbcacbddaabcdbdccdcacbdadbba"
        "dccbdddcbbcbdbbcdaabdaacbcacdbbdcdcdabcbadbcabddcadccdddcaaababccbdaaabbcbcaaabdadaabbacbbaacdddccabdcadcbcbb"
        "aacadcadabcdddabdbabdbbacbccdcbaaadabbbabcadadaddacdabbbdbdbbcddcdccbddbcacbbcccccaaccccdbadbcaccdadaabadcdcc"
        "cdaaddadccbaddbdbaaccaaacbdabdacbdadbdcddbcdddbacccaabdaaacdabccbaadbacbcbccabbbaacbccabccaabddaacdddccddbadb"
        "bbccababbbbadbcccbccdcadbdbccdcadacbadbccbcbdcccdaaccacaaccdadbcabddbbcadacacaabaaaacdcdacbbccbccdaacddddaacb"
        "daccdacbbdadabdbbdbcacbaabdaccabadbbbaacbacaccbdbacbdbcadbbabbbbdcbbbbdbcababdcbdcaaddabcaddcaabdcbbdbacddbdd"
        "bdccdacaaccadacdbdccbcbdaddcbbdababdcbbdcbcbddbadcdccaccbcabdcadcadbadaabdbcccbaddabdaacabdbabbcbaddbacdadbcc"
        "aabdbcccdca",
        864736),
]


@pytest.mark.parametrize("text,expected", testdata)
def test_1(text, expected):
    assert count_unique_substrings(text) == expected
