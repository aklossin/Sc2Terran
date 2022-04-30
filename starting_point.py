from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

class GavinDestroyer(BotAI):
    async def on_step(self, iteration:int):
        print(f"the iteration is {iteration}")

        if self.townhalls: 
            comcent = self.townhalls.random
            #make more scvs
            if comcent.is_idle and self.can_afford(UnitTypeId.SCV):
                comcent.train(UnitTypeId.SCV)
            #make supply depos to not get supply blocked
            elif self.supply_left < 3:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=comcent.position)
            #make him expand
            elif self.can_afford(UnitTypeId.COMMANDCENTER) and self.already_pending(UnitTypeId.COMMANDCENTER) < 1:
                await self.expand_now()
            #make barracks
            elif self.structures(UnitTypeId.SUPPLYDEPOT).ready:
                if self.structures(UnitTypeId.BARRACKS).amount < 3 and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):
                        await self.build(UnitTypeId.BARRACKS, near=comcent.position)
            #build from barracks
            for barracks in self.structures(UnitTypeId.BARRACKS).ready.idle:
                if self.can_afford(UnitTypeId.MARINE):
                    barracks.train(UnitTypeId.MARINE)
        else:
            if self.can_afford(UnitTypeId.COMMANDCENTER) and self.already_pending(UnitTypeId.COMMANDCENTER) < 1:
                await self.expand_now()

run_game(
    maps.get("ProximaStationLE"),
    [Bot(Race.Terran, GavinDestroyer()),
     Computer(Race.Terran, Difficulty.Hard)],
     realtime=False
)