import os
import pygame
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# инициализация Pygame:
pygame.init()
# размеры окна:
mashtab = 1 * 7 / 6
size = width, height = int(800 * mashtab), int(480 * mashtab)
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
true_over = False

# Groups
all_sprites = pygame.sprite.Group()
Mario_group = pygame.sprite.Group()
Blocks_group = pygame.sprite.Group()
Enemy_group = pygame.sprite.Group()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)


# Gero
class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(Mario_group, all_sprites)
        self.image = load_image("Mario_mini_40kh40.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.storons = []  # Список сторон в которые он идёт
        self.napravlenie = 1
        self.rost = 1
        self.padenie2 = True
        self.pryzhok = False
        self.left = True
        self.right = True
        self.sel = False
        self.stoit = False
        self.k11 = 0
        self.speed = 1.5  # Скорость
        self.neuz = 0
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.slovar_of_rost = {1: 'mario_mini_40kh40.png',
                               2: 'Mario.png', 3: 'Mario_pod_gribami.png'}

    def set_neuz(self, x):
        self.neuz = x

    def get_padenie(self):
        return self.padenie2

    def get_neuz(self):
        return self.neuz

    def get_rost(self):
        return self.rost

    def set_rost(self, r):
        x = self.rect.x
        y = self.rect.y
        k = 40 if self.rost == 1 else 0
        self.rost = r
        self.image = load_image(self.slovar_of_rost[self.rost], -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - k
        if self.napravlenie == 1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    # Обновление героя
    def update(self, *args):
        if self.neuz != 0:
            self.neuz -= 10
        if pygame.sprite.spritecollideany(self, Blocks_group):
            s = [0, 0, 0, 0, 0]
            for i in Blocks_group.sprites():
                kk = pygame.sprite.collide_mask(Gero, i)
                kk2 = pygame.sprite.collide_mask(i, Gero)
                if kk:
                    s[0] += 1
                    if self.rost == 1:
                        if kk[0] <= 2 and kk[1] != 39 and kk[1] != 0:
                            self.left = False
                        else:
                            s[2] += 1
                        if kk[0] >= 37 and kk[1] != 39 and kk[1] != 0:
                            self.right = False
                        else:
                            s[3] += 1
                        if kk[1] == 39 and kk2[0] != 39 and not (kk[1] == 39 and kk2[0] == 0 and kk[0] == 39):
                            self.padenie2 = False
                            self.stoit = True
                        if kk[1] == 0 or 0 < kk[0] < 10 and kk[1] <= 16 and not self.napravlenie or \
                                39 > kk[0] >= 30 and kk[1] <= 16 and self.napravlenie:
                            self.pryzhok = False
                    elif self.rost == 2 or self.rost == 3:
                        if kk[0] <= 2 and kk[1] != 79 and kk[1] != 0:
                            self.left = False
                        else:
                            s[2] += 1
                        if kk[0] >= 37 and kk[1] != 79 and kk[1] != 0:
                            self.right = False
                        else:
                            s[3] += 1
                        if kk[1] == 79 and kk2[0] != 39:
                            self.padenie2 = False
                            self.stoit = True
                        if kk[1] == 0 or 0 < kk[0] < 10 and kk[1] <= 16 and not self.napravlenie or \
                                39 > kk[0] >= 30 and kk[1] <= 16 and self.napravlenie:
                            self.pryzhok = False
            if s[2] == s[0]:
                self.left = True
            if s[3] == s[0]:
                self.right = True
        else:
            self.stoit = False
            self.left = True
            self.right = True
            if not self.pryzhok:
                self.padenie2 = True
        # Если нажали клавишу
        if self.pryzhok and self.k11 != 1700:
            self.k11 += 10
        elif self.k11 == 1700:
            self.k11 = 0
            self.pryzhok = False
            self.padenie2 = True
        elif not self.pryzhok and 0 < self.k11 < 1700:
            self.k11 = 0
            if not self.stoit:
                self.padenie2 = True
        elif not self.pryzhok:
            self.k11 = 0
        if args[0].type == pygame.KEYDOWN:
            if args[0].key == 119 or args[0].key == 273 or args[0].key == 32:
                # 'w'
                if not self.padenie2:
                    self.pryzhok = True
                    self.stoit = False
            elif args[0].key == 115 or args[0].key == 274:
                # 's'
                self.sel = True
            elif args[0].key == 100 or args[0].key == 275:
                # 'd'
                self.storons.append(args[0])
            elif args[0].key == 97 or args[0].key == 276:
                # 'a'
                self.storons.append(args[0])
        # Если клавишу отпустили
        elif args[0].type == pygame.KEYUP:
            if args[0].key == 119 or args[0].key == 273 or args[0].key == 32:
                # 'w'
                self.pryzhok = False
            elif args[0].key == 115 or args[0].key == 274:
                # 's'
                self.sel = False
            elif args[0].key == 100 or args[0].key == 275:
                # 'd'
                for key in self.storons:
                    if key.key == args[0].key:
                        self.storons.remove(key)
            elif args[0].key == 97 or args[0].key == 276:
                # 'a'
                for key in self.storons:
                    if key.key == args[0].key:
                        self.storons.remove(key)

    # Функция движения
    def Moving(self):
        if self.pryzhok:
            # 'w'
            self.rect.y -= self.speed
        if self.sel:
            # 's'
            pass
        if self.padenie2:
            if self.rect.y + self.speed < height:
                self.rect.y += self.speed
            else:
                self.kill()
        if self.storons:
            self.storon = self.storons[-1]
            if self.storon.key == 100 or self.storon.key == 275:
                # 'd'
                if self.rect.x + self.rect[3] + self.speed <= width and self.right:
                    self.rect.x += self.speed
                if self.napravlenie == 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mask = pygame.mask.from_surface(self.image)
                self.napravlenie = 1
            elif self.storon.key == 97 or self.storon.key == 276:
                # 'a'
                if self.rect.x - self.speed >= 0 and self.left:
                    self.rect.x -= self.speed
                if self.napravlenie == 1:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.mask = pygame.mask.from_surface(self.image)
                self.napravlenie = 0


class Owl(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(Enemy_group, all_sprites)
        self.image = load_image("sova.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.padenie2 = True
        self.left = True
        self.right = False
        self.speed = 1  # Скорость
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self.rect.y >= height:
            self.kill()
        s = [0, 0, 0, 0, 0]
        bk = pygame.sprite.spritecollide(self, Blocks_group, False)
        sk = pygame.sprite.spritecollide(self, Enemy_group, False)
        kk = sk + bk
        for i in kk:
            if i != self:
                kk = pygame.sprite.collide_mask(self, i)
                if kk:
                    s[0] += 1
                    if kk[0] <= 2 and kk[1] != 39 and kk[1] != 0:
                        self.left = False
                        self.right = True
                    else:
                        s[2] += 1
                    if kk[0] >= 37 and kk[1] != 39 and kk[1] != 0:
                        self.right = False
                        self.left = True
                    if kk[1] == 39:
                        self.padenie2 = False
        if s[0] == s[4]:
            self.padenie2 = True
        if pygame.sprite.spritecollide(self, Mario_group, False):
            kk = pygame.sprite.collide_mask(self, Gero)
            if kk:
                if kk[1] <= 15 and Gero.get_padenie():
                    if not Gero.get_neuz():
                        self.kill()
                else:
                    if Gero.get_rost() == 1:
                        if not Gero.get_neuz():
                            Gero.kill()
                    else:
                        Gero.set_rost(1)
                        Gero.set_neuz(1000)

    def Moving(self):
        if self.padenie2:
            self.rect.y += 1
        if self.right:
            self.rect.x += 1
        if self.left:
            self.rect.x -= 1


list_of_blocks = {'pol': "pol.png", 'kir-i': "kirpichiki.png",
                  "?": 'blok_zagadka.png', '-?-': 'blok_zagadka_bez_zagadki.png',
                  'blok': 'blok.png', 'T1': 'Truba1.png', 'T2': 'Truba2.png',
                  '[': 'Truba3.png', ']': 'Truba4.png'}


# Blocks
class Blocks(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name="pol"):
        super().__init__(Blocks_group, all_sprites)
        self.image = load_image(list_of_blocks[image_name])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        pass


class Truba(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        super().__init__(Blocks_group, all_sprites)
        self.image = load_image(list_of_blocks[image_name], (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        pass


class Kirpichi(Blocks):
    def __init__(self, x, y, monetochniy=False):
        super().__init__(x, y, image_name='kir-i')
        self.monetochniy = monetochniy
        self.monetki = random.choice(range(3, 8)) if monetochniy else 0

    def update(self, *args):
        kk = pygame.sprite.collide_mask(self, Gero)
        if kk:
            if kk[1] == 39 and kk[0] >= 2 and kk[0] <= 37:
                if self.monetochniy:
                    if self.monetki > 1:
                        self.monetki -= 1
                        Monetka(self.rect.x, self.rect.y - 40)
                    elif self.monetki == 1:
                        self.monetki -= 1
                        Monetka(self.rect.x, self.rect.y - 40)
                        self.image = load_image(list_of_blocks['-?-'])
                else:
                    if Gero.get_rost() != 1:
                        self.kill()


class Block_zagadka(Blocks):
    def __init__(self, x, y, monetochniy=True):
        super().__init__(x, y, image_name='?')
        self.monetochniy = monetochniy
        self.monetki = 1 if monetochniy else 0
        self.sost = 1

    def update(self, *args):
        if self.sost:
            kk = pygame.sprite.collide_mask(self, Gero)
            if kk:
                if kk[1] == 39 and kk[0] != 0 and kk[0] != 39:
                    if self.monetochniy:
                        if self.monetki == 1:
                            self.monetki -= 1
                            Monetka(self.rect.x, self.rect.y - 40)
                            self.sost = 0
                            self.image = load_image(list_of_blocks['-?-'])
                    else:
                        if Gero.get_rost() == 1:
                            Grib(self.rect.x, self.rect.y - 40)
                            self.sost = 0
                            self.image = load_image(list_of_blocks['-?-'])
                        else:
                            Flower(self.rect.x, self.rect.y - 40)
                            self.sost = 0
                            self.image = load_image(list_of_blocks['-?-'])


class Monetka(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('monetka.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.k = 0

    def update(self, *args):
        self.k += 10
        if self.k % 80 == 0:
            self.rect.y -= 1
        if self.k == 2000:
            self.kill()


class Grib(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('Gribochek.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.k = 0

    def update(self, *args):
        if pygame.sprite.spritecollide(self, Mario_group, False):
            if Gero.get_rost() == 1:
                Gero.set_rost(2)
            self.kill()


class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('Tsvetochek.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.k = 0

    def update(self, *args):
        if pygame.sprite.spritecollide(self, Mario_group, False):
            if Gero.get_rost() == 2:
                Gero.set_rost(3)
            elif Gero.get_rost() == 1:
                Gero.set_rost(2)
            self.kill()


class Game_over(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Over_group)
        self.image = load_image('Game_over.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def update(self, *args):
        pass


class You_win(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Over_group)
        self.image = load_image('You_win.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

    def update(self, *args):
        pass


class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('zamok.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        global true_over
        if pygame.sprite.spritecollide(self, Mario_group, False):
            true_over = True


# Инициализация врагов, героя и блоков, уровень 1
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


level = load_level('lvl1_2.txt')

# level = load_level('lvl')
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == '.':
            pass
        elif level[i][j] == '#':
            Blocks(j * 40, i * 40)
        elif level[i][j] == '=':
            Kirpichi(j * 40, i * 40)
        elif level[i][j] == '$':
            Kirpichi(j * 40, i * 40, True)
        elif level[i][j] == 'B':
            Blocks(j * 40, i * 40, 'blok')
        elif level[i][j] == 'Z':
            Castle(j * 40, i * 40)
        elif level[i][j] == '?':
            Block_zagadka(j * 40, i * 40)
        elif level[i][j] == 'G':
            Block_zagadka(j * 40, i * 40, False)
        elif level[i][j] == '\\':
            Truba(j * 40, i * 40, 'T1')
        elif level[i][j] == '/':
            Truba(j * 40, i * 40, 'T2')
        elif level[i][j] == '[':
            Truba(j * 40, i * 40, '[')
        elif level[i][j] == ']':
            Truba(j * 40, i * 40, ']')
        elif level[i][j] == '@':
            Gero = Mario(j * 40, i * 40)
        elif level[i][j] == '-':
            Owl(j * 40, i * 40)

# ожидание закрытия окна:
camera = Camera()
clock = pygame.time.Clock()
MYEVENTTYPE = 1
k = 0
pygame.time.set_timer(MYEVENTTYPE, 10)
running = True
screen.fill((114, 208, 237))
while running and not true_over:
    if not Gero.alive():
        true_over = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            Gero.kill()
        if event.type == MYEVENTTYPE:
            k += 10
            Gero.Moving()
            for j in Enemy_group:
                j.Moving()
        # изменяем ракурс камеры
        camera.update(Gero)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update(event)
    screen.fill((114, 208, 237))
    Mario_group.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(90)
Over_group = pygame.sprite.Group()
Over = Game_over() if not Gero.alive() else You_win()
# завершение работы:
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Over.update()
    Over_group.draw(screen)
    pygame.display.flip()
pygame.quit()
