__author__ = 'teemu kanstren'

def unify_line_separators(line):
    line = line.replace("\r\n", "\n")
    line = line.replace("\r", "\n")
    return line

def equal(actual, expected):
    actual = unify_line_separators(actual)
    expected = unify_line_separators(expected)
    msg = "'"+expected+"' != '"+actual+"'"
#    msg = "Expected: '"+expected+"'\n"
#    msg += "Actual: '"+actual+"'"
    assert actual == expected, msg

