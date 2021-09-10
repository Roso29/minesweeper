from minesweeper.main import *

def test_too_many_rows():
    try:
        field = Field(101,5)
        assert False
    except WrongDimensionsGiven:
        assert True

def test_0_rows():
    try:
        field = Field(0,5)
        assert False
    except WrongDimensionsGiven:
        assert True

def test_too_many_columns():
    try:
        field = Field(5,101)
        assert False
    except WrongDimensionsGiven:
        assert True

def test_0_columns():
    try:
        field = Field(5,0)
        assert False
    except WrongDimensionsGiven:
        assert True

def test_row_too_short():
    field = Field(4,5)
    try:
        field.map.AddRow('..*')
        assert False
    except RowWrongSize:
        assert True

def test_row_too_long():
    field = Field(4,5)
    try:
        field.map.AddRow('..*..*')
        assert False
    except RowWrongSize:
        assert True

def test_too_many_columns():
    field = Field(4,5)
    try:
        field.map.AddRow('..*..')
        field.map.AddRow('..*..')
        field.map.AddRow('..*..')
        field.map.AddRow('..*..')
        field.map.AddRow('..*..')
        assert False
    except ColumnsWrongSize:
        assert True

def test_valid_characters_used():
    field = Field(4,5)
    try:
        field.map.AddRow('..A.*')
        assert False
    except InvalidSymbol:
        assert True

def test_convert_row_to_objects():
    field = Field(1,5)
    field.map.AddRow('..*..')
    assert field.map.mapArray == [[SafeSpot(),SafeSpot(),Mine(),SafeSpot(),SafeSpot()]]


def test_simple_row_counts():
    field = Field(1,5)
    field.map.AddRow('..*..')
    field.GenerateHints()
    hints = field.map.StringifyObjectMap()
    assert hints == [['0','1','*','1','0']]

def test_field_count_one_mine():
    field = Field(3,3)
    field.map.AddRow('..*')
    field.map.AddRow('...')
    field.map.AddRow('...')
    field.GenerateHints()
    hints = field.map.StringifyObjectMap()
    assert hints == [['0','1','*'],
                     ['0','1','1'],
                     ['0','0','0']]

def test_field_count_many_mines():
    field = Field(4,4)
    field.map.AddRow('*...')
    field.map.AddRow('....')
    field.map.AddRow('.*..')
    field.map.AddRow('....')
    field.GenerateHints()
    hints = field.map.StringifyObjectMap()
    assert hints == [['*','1','0','0'],
                     ['2','2','1','0'],
                     ['1','*','1','0'],
                     ['1','1','1','0']]