class RowWrongSize(Exception):
    """Raised when the row entered by user is different length to number of columns required"""
    pass

class ColumnsWrongSize(Exception):
    """Raised when too many rows are added to the field"""
    pass

class InvalidSymbol(Exception):
    """Raised when a row provided contains symbols other than * or ."""

class WrongDimensionsGiven(Exception):
    """Raised when user requests field of size NxM where N,M>100 or N,M=<0"""


class Field:
    def __init__(self,rows,columns):
        self.rows=rows
        self.columns=columns
        self.map = self.CreateMap(rows,columns)

    def CreateMap(self,rows,columns):
        if (not self.IsSizeValid(rows,columns)):
            raise WrongDimensionsGiven
        else:
            return Map(rows,columns)

    def IsSizeValid(self,rows,columns):
        isRowValid = rows<=100 and rows>0
        isColumnValid = columns <= 100 and columns>0
        return isRowValid and isColumnValid

    def GenerateHints(self):
        for row in range(self.rows):
            for column in range(self.columns):
                square = self.map.mapArray[row][column]
                if square.visual == '*':
                    continue
                mineCount = self.CalculateMineCount(row,column)
                square.visual = str(mineCount)

    def CalculateMineCount(self, row, column):
        rowRanges = list(set([max(0,row-1),row,min(self.rows-1,row+1)]))
        columnRanges = list(set([max(0,column-1),column,min(self.columns-1,column+1)]))
        mineCount = 0
        for rOffset in rowRanges:
            for cOffset in columnRanges:
                mineCount+=isinstance(self.map.mapArray[rOffset][cOffset],Mine)

        return mineCount


class Map:
    def __init__(self, rows, columns):
        self.mapArray = []
        self.rows = rows
        self.columns = columns

    def AddRow(self, rowString):
        self.ValidateRowString(rowString)
        rowObjs = self.GenSquareObjects(rowString)
        self.mapArray.append(rowObjs)

    def GenSquareObjects(self, rowString):
        squareObjects = [SafeSpot() if square == '.' else Mine() for square in rowString]
        return squareObjects

    def StringifyObjectMap(self):
        stringMapArray = self.mapArray.copy()
        for row in range(self.rows):
            for column in range(self.columns):
                stringMapArray[row][column] = str(self.mapArray[row][column])
        return stringMapArray

    def MapToString(self, stringMapArray):
        mapString = ''
        for row in stringMapArray:
            mapString += ''.join(row)+'\n'
        return mapString
    #Validation Functions

    def ValidateRowString(self, rowString):
        if not self.IsRowSizeValid(rowString):
            raise RowWrongSize
        if not self.IsColumnSizeValid():
            raise ColumnsWrongSize
        if not self.IsValidSymbol(rowString):
            raise InvalidSymbol

    def IsRowSizeValid(self, rowString):
        return len(rowString) == self.columns

    def IsColumnSizeValid(self):
        return len(self.mapArray)<self.rows

    def IsValidSymbol(self, rowString):
        correctSymbols = all([symbol in ['.','*'] for symbol in rowString])
        return correctSymbols


class SafeSpot:
    def __init__(self):
        self.visual = '.'

    def __repr__(self):
        return self.visual

    def __eq__(self,other):
        return self.visual == other.visual


class Mine:
    def __init__(self):
        self.visual = '*'

    def __repr__(self):
        return self.visual

    def __eq__(self,other):
        return self.visual == other.visual


if __name__ == "__main__":
    sizes = input()
    fieldNum = 1
    outputDict = {}

    while sizes != '0 0':
        rows = int(sizes[0])
        columns = int(sizes[2])
        field = Field(rows,columns)
        for iRow in range(rows):
            rowString = input()
            field.map.AddRow(rowString)
        field.GenerateHints()
        hintsArray = field.map.StringifyObjectMap()
        outputDict[fieldNum]=field.map.MapToString(hintsArray)
        fieldNum+=1
        sizes = input()

    for i in range(1,fieldNum+1):
        print("Field#"+str(i))
        print(outputDict[i])
