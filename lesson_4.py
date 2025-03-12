from random import randint, choice

class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health}, damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes: list):
        random_hero = choice(heroes)
        self.__defence = random_hero.ability

    def attack(self, heroes: list):
        for hero in heroes:
            if hero.health > 0:
                if hasattr(hero, 'is_protected') and hero.is_protected:
                    print(f'{hero.name} is protected and takes no damage!')
                    hero.is_protected = False  # Сбрасываем защиту после раунда
                elif type(hero) == Berserk and self.defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= self.damage - hero.blocked_damage
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + ' defence: ' + str(self.__defence)


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability
        self.is_protected = False  # Добавляем атрибут защиты

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss: Boss):
        boss.health -= self.damage

    def apply_super_power(self, boss: Boss, heroes: list):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss: Boss, heroes: list):
        crit = self.damage * randint(2, 5)
        boss.health -= crit
        print(f'Warrior {self.name} hit critically: {crit}')


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOSTING')
        self.rounds_active = 4
        self.boost_value = 5

    def apply_super_power(self, boss: Boss, heroes: list):
        if self.rounds_active > 0:
            for hero in heroes:
                if hero.health > 0:
                    hero.damage += self.boost_value
            self.rounds_active -= 1
            print(f'Magic {self.name} boosted heroes by {self.boost_value}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss: Boss, heroes: list):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted: {self.__blocked_damage}')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'REVIVE')
        self.used_revive = False

    def attack(self, boss: Boss):
        pass

    def apply_super_power(self, boss: Boss, heroes: list):
        if not self.used_revive:
            for hero in heroes:
                if hero.health == 0:
                    hero.health = self.health
                    self.health = 0
                    self.used_revive = True
                    print(f'Witcher {self.name} revived {hero.name} and died')
                    break


class Hacker(Hero):
    def __init__(self, name, health, damage, steal_amount):
        super().__init__(name, health, damage, 'STEAL_HEALTH')
        self.steal_amount = steal_amount
        self.rounds_counter = 0

    def apply_super_power(self, boss: Boss, heroes: list):
        self.rounds_counter += 1
        if self.rounds_counter % 2 == 0 and boss.health > 0:
            alive_heroes = [hero for hero in heroes if hero.health > 0]
            if alive_heroes:
                boss.health -= self.steal_amount
                lucky_hero = choice(alive_heroes)
                lucky_hero.health += self.steal_amount
                print(f'Hacker {self.name} украл {self.steal_amount} и отдал {lucky_hero.name}')


class Kamikadze(Hero):
    def __init__(self, name, health):
        super().__init__(name, health, 0, 'KAMIK')
        self.used_explosion = False

    def apply_super_power(self, boss: Boss, heroes: list):
        if not self.used_explosion and self.health > 0:
            hit_chance = randint(0, 1)
            if hit_chance:
                boss.health -= self.health
                print(f'Kamikadze {self.name} взрывается с шансом {self.health}')
            else:
                boss.health -= self.health // 2
                print(f'Kamikadze {self.name} промахнулся и нанёс {self.health // 2}')
            self.health = 0
            self.used_explosion = True


class Avenger(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'PROTECTION')

    def apply_super_power(self, boss: Boss, heroes: list):
        if randint(1, 100) <= 20:
            for hero in heroes:
                if hero.health > 0:
                    hero.is_protected = True
            print(f'Avenger {self.name} защитил всю команду')


round_number = 0


def show_statistics(boss: Boss, heroes: list):
    print(f'ROUND {round_number} ----------------')
    print(boss)
    for hero in heroes:
        print(hero)


def is_game_over(boss: Boss, heroes: list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def play_round(boss: Boss, heroes: list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def start_game():
    boss = Boss('Splinter', 1000, 50)
    warrior_1 = Warrior('Django', 280, 10)
    warrior_2 = Warrior('Billy', 270, 15)
    magic = Magic('Dulittle', 290, 10)
    doc = Medic('James', 250, 5, 15)
    assistant = Medic('Marty', 300, 5, 5)
    berserk = Berserk('William', 260, 10)
    witcher = Witcher('Geralt', 300, 0)
    hacker = Hacker('Neo', 250, 10, 20)
    kamikadze = Kamikadze('Kami', 400)
    avenger = Avenger('Toь', 280, 15)

    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, kamikadze, avenger]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()