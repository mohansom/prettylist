# Copyright 2009 lacewing.cc@outlook.com
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'A simple Python library for easily displaying tabular data in a visually appealing ASCII table format'

__version__ = '0.1.9'

F_LEFT = 'F_LEFT'
F_CENTER = 'F_CENTER'
F_RIGHT = 'F_RIGHT'
F_DEFAULT = 'F_DEFAULT'


class Column:
    """Return a new Column instance.

    :param header: string of the name of column
    :param fmt: the describe of alignment. F_LEFT for left, F_CENTER for centre, F_RIGHT for right and F_DEFAULT for automatically selects the best
    """

    def __init__(self, header, fmt=F_DEFAULT):
        self.header = header
        self.fmt = fmt
        if self.fmt not in [F_LEFT, F_CENTER, F_RIGHT, F_DEFAULT]:
            raise ValueError('invalid fmt: %s' % self.fmt)
        self.width = 0


class PrettyList:
    """Return a new PrettyList instance.

    :param columns: list of object Column
    :param noheader: if this value is true, a header line isn't generated
    :param sort: header of column for sort by
    :param reverse: the reverse flag can be set to request the result in descending order
    :param sep: delimiter between fields
    :param linesep: delimiter between lines
    """

    def __init__(self, columns, noheader=True, sort=None, reverse=False, sep=' ', linesep='\n'):
        if not isinstance(columns, (list, tuple)) or len(columns) == 0:
            raise ValueError('invalid columns: %s' % columns)
        self.columns = columns
        self.columns_headers = [c.header for c in self.columns]
        self.rows = []
        self.noheader = noheader
        self.sort = sort
        self.reverse = reverse
        self.sep = sep
        self.linesep = linesep

    def __str__(self):
        return self[:]

    def __getitem__(self, index):
        """Return a string by self[start:stop:step]"""
        if self.sort:
            pos = self.columns_headers.index(self.sort)
            self.rows.sort(key=lambda _: _[pos], reverse=self.reverse)

        subrows = self.rows[index]
        if isinstance(index, int):
            subrows = [subrows]

        for row in subrows:
            for index, entry in enumerate(row):
                self.columns[index].width = max(self.columns[index].width, len(convert_to_string(entry)))
        if not self.noheader:
            for column in self.columns:
                column.width = max(column.width, len(column.header))

        lines = []
        if not self.noheader:
            lines.append(self._generate_line(self.columns_headers))
            lines.append(self._generate_line([column.width * '-' for column in self.columns]))
        for row in subrows:
            lines.append(self._generate_line(row))

        return self.linesep.join(lines)

    def _generate_line(self, row):
        """Return a formatted string of row by columns"""
        row = list(map(convert_to_string, row))
        units = []
        for index, entry in enumerate(row[:-1]):
            column = self.columns[index]
            fmt = column.fmt
            if fmt == F_DEFAULT:
                fmt = F_LEFT if index == 0 else F_RIGHT
            unit = {
                F_LEFT: str.ljust,
                F_CENTER: str.center,
                F_RIGHT: str.rjust
            }.get(fmt)(entry, column.width)
            units.append(unit)
        units.append(row[-1])
        return self.sep.join(units)

    def add_row(self, row):
        """Add a row to the list. If the header has been set, the length of date
        should be consistent with header.

        :param row: list or tuple of data
        """
        if len(row) > len(self.columns):
            raise ValueError('invalid row: %s' % row)
        self.rows.append(row)


def convert_to_string(instance):
    return str(instance)


if __name__ == '__main__':
    p = PrettyList([
        Column(header='City name'),
        Column(header='Area', fmt=F_RIGHT),
        Column(header='Population'),
        Column(header='Annual Rainfall')
    ], noheader=False, sort='City name', sep=' | ')

    p.add_row(['Adelaide', 1295, 1158259, 600.5])
    p.add_row(['Brisbane', 5905, 1857594, 1146.4])
    p.add_row(['Darwin', 112, 120900, 1714.7])
    p.add_row(['Hobart', 1357, 205556, 619.5])
    p.add_row(['Sydney', 2058, 4336374, 1214.8])
    p.add_row(['Melbourne', 1566, 3806092, 646.9])
    p.add_row(['Perth', 5386, 1554769, 869.4])

    print(p)
