import discord
import random
import json
import asyncio
from discord.ext import commands
import yaml
from Character.Main_Char import Adventurer, Enemy





class Main(commands.Cog, discord.Client) :
    def __init__(self, bot):
        self.bot = bot
    async def dumpJson(self, json_object) :
        a_file = open("Database/empty.json", "w")
        json.dump(json_object, a_file)
        a_file.close()
    async def getJson(self) :
        a_file = open("Database/empty.json", "r")
        json_object = json.load(a_file)
        a_file.close()

        return json_object
    async def hasAccount(self, userid) :
        json_object = await self.getJson()

        if str(userid) in json_object :
            return True
        return False
    async def getResponse(self, ctx, start_message, check_func, time_out_message = 'Sorry, your response took too long', time = 30) :
        response = ""
        try:
            await ctx.send(start_message)
            response = await bot.wait_for('message', check=check_func, timeout=time)
        except asyncio.TimeoutError:
            await ctx.channel.send(time_out_message)
            
            return response

        return response
    async def getYamlDungeon(self) :
        a_file = open("Stage/stage.yml", "r")
        yaml_object = yaml.load_all(a_file, Loader=yaml.FullLoader)

        dungeon = {}
        for data in yaml_object :
            dungeon = data

        a_file.close()
        return dungeon
    async def thereIsStage(self, stage) :
        dungeon = await self.getYamlDungeon()
        return stage <= list(dungeon[list(dungeon.keys())[-1]])[-1]
    async def getEnemy(self, stage) :
        dungeon = await self.getYamlDungeon()
        floor_name = -1
        floor_value = -1
        for floor_name in dungeon :
            for floor_value in dungeon[floor_name] :
                if floor_value == stage :
                    break
            else :
                continue
            break

        
        enemie_entity = None
        enemies_yaml = yaml.load_all(open("Enemies/enemies.yml"), Loader=yaml.FullLoader)
        for enemies in enemies_yaml :
                enemie_entity = enemies
        enemy = [[], []]
        for item in dungeon[floor_name][floor_value] :
            for _ in range(int(item.split()[0])) :
                temp_enemy = Enemy(fname = item.split()[1].replace("_", " "), level = int(item.split()[2]), **enemie_entity[item.split()[1]])
                enemy[0].append(temp_enemy)
                enemy[1].append(temp_enemy.health)

        #       class enemy                                  darah dari class enemy
        return [enemy[0], [dungeon[floor_name][floor_value], enemy[1]]]
    async def battle(self, battle_audience, ctx, monster_list, json_object) :
        

        await ctx.send("Battle has started\n" +"\n".join([f"You encounter {' '.join(monster_list[0][a].split(' ')[0:2]).replace('_', ' ')} level {''.join(monster_list[0][a].split(' ')[2])} dengan darah {monster_list[1][a]}" for a in range(len(monster_list[0]))]))
        battle_audience.append(Adventurer(**json_object[str(ctx.message.author.id)]))
        battle_audience = sorted(battle_audience, key= lambda e:e.agil, reverse=True)
        def isStr(m):
                return m.author == ctx.author and m.content == 'n' or m.content == 'y'


        def isNum(m):
                return m.author == ctx.author and m.content.isnumeric()
        
        player_index = []
        total_hp_adventurer = 0
        total_hp_enemy = 0
        display = []
        for j in range(len(battle_audience)) :
            if isinstance(battle_audience[j], Adventurer) :
                player_index.append(j)
                total_hp_adventurer += battle_audience[j].health
                display.append(f'{j}. {battle_audience[j].fname}')
            else :
                total_hp_enemy += battle_audience[j].health
                display.append(f'{j}. {battle_audience[j].fname}')
        

        i = 0
        while True :
            # kalo mau ada dps dikurangin dlu darahnya sebelum if dibawah ini
            if i in player_index and battle_audience[i].health > 0 :
                # Tinggal ubah ctx menjadi sesuai dengan player index dan userid supaya bisa multiplayer
                await ctx.send('\n'.join(display))
                number = await self.getResponse(ctx, "choose index number enemy to take action? ", isNum)

                if hasattr(number, 'content') :
                    if int(number.content) >= 0 and int(number.content) < len(battle_audience) :
                        answer = await self.getResponse(ctx, "do you want to attack? (y/n) ", isStr)

                        try :
                            if answer.content == 'y' :
                                output_damage = battle_audience[i].damage_output()
                                await ctx.send(battle_audience[int(number.content)].attacked(output_damage))
                                if int(number.content) in player_index :
                                    total_hp_adventurer -= output_damage
                                else :
                                    total_hp_enemy -= output_damage
                        except :
                            pass
            elif battle_audience[i].health <= 0 :
                pass
            else :
                output_damage = battle_audience[i].damage_output()
                await ctx.send(battle_audience[random.choice(player_index)].attacked(battle_audience[i].damage_output()))
                total_hp_adventurer -= output_damage
                
            
            if total_hp_adventurer <= 0 :
                return 'lose'
            elif total_hp_enemy <= 0 :
                return 'win'
            else :
                pass

            if i < len(battle_audience)-1 :
                i += 1
            else :
                i = 0
    @commands.command()
    async def create_account(self, ctx, *, nickname) :
        json_object = await self.getJson()

        if await self.hasAccount(str(ctx.message.author.id)) :
            await ctx.send('you\'ve already create account!')
            return False

        hero = Adventurer(fname = nickname)
        json_object[ctx.message.author.id] = hero.__dict__

        await self.dumpJson(json_object)
        del hero
        await ctx.send('your account successfully created!')

    @commands.command()
    async def del_account(self, ctx) :
        json_object = await self.getJson()

        if not await self.hasAccount(str(ctx.message.author.id)) :
            await ctx.send('you don\'t have an account!')
            return False

        del json_object[str(ctx.message.author.id)]

        await self.dumpJson(json_object)
        await ctx.send('your account successfully deleted!')

    @commands.command()
    async def profile(self, ctx) :
        json_object = await self.getJson()

        if not await self.hasAccount(str(ctx.message.author.id)) :
            await ctx.send('you don\'t have an account!')
            return False
            
        await ctx.send(json_object[str(ctx.message.author.id)])
    @commands.command()
    async def test(self, ctx) :

        if not await self.hasAccount(str(ctx.message.author.id)) :
            await ctx.send('you don\'t have an account please create one!')
            return False

        json_object = await self.getJson()
        stage = json_object[str(ctx.message.author.id)]['stage']

        if not await self.thereIsStage(stage) :
            await ctx.send('The stage not builded yet...')

        def isStr(m):
                return m.author == ctx.author and m.content == 'n' or m.content == 'y' 

        answer = await self.getResponse(ctx, "Do you wan't to start dungeon? (y/n) ", isStr)

        if answer == "" or answer.content == 'n':
            await ctx.send("back to menu..")
            return False

        battle_audience, monster_list= await self.getEnemy(2)
        await ctx.send(await self.battle(battle_audience, ctx, monster_list, json_object))

bot = commands.Bot(command_prefix=("/"))
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    
bot.add_cog(Main(bot))
bot.run('insert your token here')