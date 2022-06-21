class Item:
    def __init__(self, value: int, domain: list = []) -> None:
        self.v = value
        self.d = domain
        self.neighbor = 0

    def domain(self, n: int, m: list = [0]) -> None:
        self.d = [i for i in range(1, n+1) if i not in m]


class Table:
    def __init__(self, table: list, n: int) -> None:
        self.t = table
        self.n = n
        self.c = 0

    def printArr(self) -> None:
        for row in self.t:
            for col in row:
                print(col.v, end=' ')
            print()

    def add_queue(self) -> list:
        table = self.t
        queue = [(table[i][j], i, j) for i in range(self.n)
                 for j in range(self.n) if table[i][j].v == 0]
        return queue

    def MRV(self) -> tuple:
        queue = self.add_queue()
        queue.sort(key=lambda x: len(x[0].d), reverse=True)
        return queue.pop()

    def degree(self) -> tuple:
        queue = self.add_queue()
        queue.sort(key=lambda x: x[0].neighbor)
        return queue.pop()

    def findZero(self) -> tuple:
        table = self.t
        for i in range(self.n):
            for j in range(self.n):
                if table[i][j].v == 0:
                    return (i, j)
        return(-1, -1)

    def isSafe(self, row: int, col: int, choice: int) -> bool:
        table = self.t
        for i in range(self.n):
            if table[row][i].v == choice or table[i][col].v == choice:
                return False
        return True

    def update(self, row: int, col: int) -> None:
        ex = []
        table = self.t
        for i in range(self.n):
            if table[i][col].v != 0:
                ex.append(table[i][col].v)
            elif table[row][i].v != 0:
                ex.append(table[row][i].v)
        table[row][col].domain(self.n, ex)

    def neighbor_update(self, row: int, col: int) -> None:
        table = self.t
        counter = 0
        if row == 0:
            if table[row+1][col].v == 0:
                counter += 1
            if col == 0:
                if table[row][col+1].v == 0:
                    counter += 1
                if table[row+1][col+1].v == 0:
                    counter += 1
            elif col == self.n-1:
                if table[row][col-1].v == 0:
                    counter += 1
                if table[row+1][col-1].v == 0:
                    counter += 1
            else:
                if table[row+1][col-1].v == 0:
                    counter += 1
                if table[row+1][col+1].v == 0:
                    counter += 1
                if table[row][col-1].v == 0:
                    counter += 1
                if table[row][col+1].v == 0:
                    counter += 1
        elif row == self.n-1:
            if table[row-1][col].v == 0:
                counter += 1
            if col == self.n-1:
                if table[row][col-1].v == 0:
                    counter += 1
                if table[row-1][col-1].v == 0:
                    counter += 1
            elif col == 0:

                if table[row][col+1].v == 0:
                    counter += 1
                if table[row-1][col+1].v == 0:
                    counter += 1
            else:
                if table[row-1][col-1].v == 0:
                    counter += 1
                if table[row-1][col+1].v == 0:
                    counter += 1
                if table[row][col-1].v == 0:
                    counter += 1
                if table[row][col+1].v == 0:
                    counter += 1
        elif col == 0:
            if table[row-1][col].v == 0:
                counter += 1
            if table[row+1][col].v == 0:
                counter += 1
            if table[row][col+1].v == 0:
                counter += 1
            if table[row+1][col+1].v == 0:
                counter += 1
            if table[row-1][col+1].v == 0:
                counter += 1
        elif col == self.n-1:
            if table[row-1][col].v == 0:
                counter += 1
            if table[row+1][col].v == 0:
                counter += 1
            if table[row][col-1].v == 0:
                counter += 1
            if table[row+1][col-1].v == 0:
                counter += 1
            if table[row-1][col-1].v == 0:
                counter += 1
        else:
            if table[row-1][col-1].v == 0:
                counter += 1
            if table[row-1][col].v == 0:
                counter += 1
            if table[row-1][col+1].v == 0:
                counter += 1
            if table[row][col-1].v == 0:
                counter += 1
            if table[row][col+1].v == 0:
                counter += 1
            if table[row+1][col-1].v == 0:
                counter += 1
            if table[row+1][col].v == 0:
                counter += 1
            if table[row+1][col+1].v == 0:
                counter += 1

        table[row][col].neighbor = counter

    def update_all(self) -> None:
        for row in range(self.n):
            for col in range(self.n):
                self.update(row, col)
                self.neighbor_update(row, col)

    def solve(self, heurestic) -> bool:
        self.c += 1
        table = self.t
        if self.findZero() == (-1, -1):
            return True
        item = heurestic()
        location = (item[1], item[2])
        for i in item[0].d:
            if self.isSafe(location[0], location[1], i):
                table[location[0]][location[1]].v = i
                self.update_all()
                if self.solve(heurestic=self.MRV):
                    return True
                else:
                    table[location[0]][location[1]].v = 0
                    self.update_all()

        return False


def main() -> None:
    n = int(input())
    arr = [[0 for _ in range(n)]for _ in range(n)]
    for i in range(n):
        inp = list(map(int, input().split()))
        for j in range(n):
            item = Item(inp[j])
            if inp[j] == 0:
                item.domain(n)
            arr[i][j] = item
    table = Table(arr, n)
    table.update_all()
    if table.solve(table.degree):
        print('---------------------')
        table.printArr()
        print(table.c)
        print('Solved')
    else:
        print('---------------------')
        table.printArr()
        print(table.c)
        print('Not Solved!')


if __name__ == '__main__':
    main()
