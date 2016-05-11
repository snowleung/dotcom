# coding:utf-8
import random


class BoardCell():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, cell):
        return self.x == cell.x and self.y == cell.y


class Board():

    '''
    战场
    '''

    def __init__(self, size=7):
        self.lands = []
        self.dotcoms = []
        self.used = set()
        self.length = size * size
        for l in 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()[:7]:
            for i in range(size):
                self.lands.append(BoardCell(l, i))

    def get_location(self, groups=3):
        _group = []
        while(len(_group) != groups):
            position = random.randint(0, self.length - 1)
            cell = self.lands[position]
            if cell not in self.used:
                self.used.add(cell)
                _group.append(cell)
        return _group

    def join_war(self, dotcom):
        self.dotcoms.append(dotcom)

    def get_all_coms(self):
        return self.dotcoms

    def is_all_sunk(self):
        for dotcom in self.dotcoms:
            if False == dotcom.is_sunk():
                return False
        return True


class DotCom(object):

    def __init__(self, name):
        self.name = name
        self.body = [[None, False], [None, False], [None, False]]  # [位于战场的位置(join的时候会更新), 是否被击中]

    def join_war(self, war):
        locations = war.get_location(len(self.body))
        for idx, body in enumerate(self.body):
            body[0] = locations[idx]
        war.join_war(self)

    def is_hit(self, point):
        for body in self.body:
            if point.equals(body[0]):
                body[1] = True  # 击中了
                return True
        return False

    def is_sunk(self):
        for body in self.body:
            if False == body[1]:
                return False
        return True


class God(object):

    @staticmethod
    def print_all_com(war):
        dot_coms = war.get_all_coms()
        for dot_com in dot_coms:
            for b in dot_com.body:
                print '{} ({},{}) {}'.format(dot_com.name, b[0].x, b[0].y, b[1])


def main():
    bullets = 10
    war = Board()
    go2_com = DotCom('Go2.com')
    go2_com.join_war(war)

    pets_com = DotCom('Pets.com')
    pets_com.join_war(war)

    askme_com = DotCom('askme.com')
    askme_com.join_war(war)

    print 'game start'
    is_win = False
    while(bullets and not is_win):
        God.print_all_com(war)
        _raw = raw_input()    # string
        for dot_com in war.get_all_coms():
            point_in_fall = BoardCell(str(_raw[0]).upper(), int(_raw[1]))
            if dot_com.is_hit(point_in_fall):
                if dot_com.is_sunk():
                    if war.is_all_sunk():
                        print 'you win'
                        is_win=True
                        break
                    else:
                        print 'sunk'
                else:
                    print 'hit'
            else:
                print 'miss'    # BUG:不应该每个都执行一次MISS


if __name__ == '__main__':
    main()
