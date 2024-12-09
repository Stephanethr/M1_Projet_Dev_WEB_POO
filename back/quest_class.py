class Quest:
    """ class to manage quests """

    def __init__(self, targs):
        self._lAvatar = targs['lAvatar']
        self._lvl = targs['lvl']
        self._itemGift = targs['gift']

    def run(self, hero):
        round = 1
        output = ""

        if len(self._lAvatar) == 1:
            output += "### PVP MODE ####\n"
            player = self._lAvatar[0]
            output += f"{player._nom} VS {hero._nom}\n"

            while player._life > 0 and hero._life > 0:
                output += f"Round {round}\n"
                output += f"PV de {hero._nom}: {hero._life}\n"
                output += f"PV de {player._nom}: {player._life}\n"

                if player.initiative() > hero.initiative():
                    output += f"{player._nom} begin\n"
                    hero.defense(player.damages())
                    if hero._life <= 0:
                        output += f"{player._nom} win\n"
                    else:
                        player.defense(hero.damages())
                else:
                    output += f"{hero._nom} begin\n"
                    player.defense(hero.damages())
                    if player._life <= 0:
                        output += f"{hero._nom} win\n"
                    else:
                        hero.defense(player.damages())

                round += 1

            if hero._life <= 0:
                output += f"{player._nom} win\n"
                player.setXP(10 * self._lvl)
                player._bag.addItem(self._itemGift)
            else:
                output += f"{hero._nom} win\n"
                hero.setXP(10 * self._lvl)
                hero._bag.addItem(self._itemGift)

        else:
            output += "### Quest MODE ####\n"
            for player in self._lAvatar:
                output += f"{player._nom} VS {hero._nom}\n"

                while player._life > 0 and hero._life > 0:
                    output += f"Round {round}\n"
                    output += f"PV de {hero._nom}: {hero._life}\n"
                    output += f"PV de {player._nom}: {player._life}\n"

                    if player.initiative() > hero.initiative():
                        output += f"{player._nom} begin\n"
                        tmpDegats = player.damages()
                        hero.defense(tmpDegats)
                        output += f"{player._nom} degats: {tmpDegats}\n"
                        if hero._life <= 0:
                            output += f"{player._nom} win\n"
                        else:
                            tmpDegats = hero.damages()
                            player.defense(tmpDegats)
                            output += f"{hero._nom} degats: {tmpDegats}\n"
                    else:
                        output += f"{hero._nom} begin\n"
                        tmpDegats = hero.damages()
                        player.defense(tmpDegats)
                        output += f"{hero._nom} degats: {tmpDegats}\n"
                        if player._life <= 0:
                            output += f"{hero._nom} win\n"
                        else:
                            tmpDegats = player.damages()
                            hero.defense(tmpDegats)
                            output += f"{player._nom} degats: {tmpDegats}\n"

                    round += 1

            if hero._life <= 0:
                output += "You lose\n"
            else:
                output += f"{hero._nom} win\n"
                hero.setXP(10 * len(self._lAvatar) * self._lvl)
                hero._bag.addItem(self._itemGift)

        return output

    def __str__(self):
        return str(self._itemGift)
