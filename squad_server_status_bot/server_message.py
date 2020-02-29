import discord
from steam import SteamQuery


async def get_server_embed(server):
    '''Queries the server information and creates a Discord embed for it.'''

    server_info = SteamQuery(server.host, server.qport).query_game_server()
    quicklink = f"{server.host}:{server.qport}"

    if not server_info["online"]:
        # Server offline, use fallback name
        embed = discord.Embed(title=server.fallback_name, color=0x222222)
        embed.add_field(name="Status", value="Offline")
        return embed

    # Create embed
    embed = discord.Embed(title=server_info["name"])

    # Thumbnail
    map = server_info['map']
    map_url_name = translate_map_name(map)
    embed.set_thumbnail(url=f"https://squadmaps.com/full/{map_url_name}.jpg")

    # Player count
    # extra formatting for queue
    # PLAYER_COUNT / MAX_PLAYERS (+ QUEUE)
    players = min(server_info["max_players"], server_info["players"])
    queue = server_info['players'] - server_info['max_players']
    player_count_str = f"{players}/{server_info['max_players']}"
    if queue > 0:
        player_count_str += f" (+{queue})"
    embed.add_field(name='Player Count', value=player_count_str)
    embed.color = get_embed_color(players)

    # Map, Quicklink
    embed.add_field(name='Map', value=f"{map}", inline=True)
    embed.add_field(name='Quick Connect', value=f"steam://connect/{quicklink}", inline=False)

    # Dynamic image
    #with open(r"images/bg1.jpg", "rb") as f:
    #    shit = await channel.send(file=f)
    #print(shit)

    return embed


def translate_map_name(name):
    '''Translates map names supplied by SteamQuery into their file names on
    squadmaps.com'''
    # Strip prefixes
    name = name.replace("CAF_", "")
    name = name.replace("SPM_", "")
    name = name.replace("HC_", "")

    # Replace spaces
    name = name.replace(" ", "_")

    # Change some map names
    name = name.replace("LogarValley", "Logar_Valley")
    name = name.replace("FoolsRoad_AAS_v2", "Fool's_Road_AAS_v1")

    return name


def get_embed_color(player_count):
    if player_count >= 41:
        return 0x20EE50 # GREEN, popped
    if player_count >= 1:
        return 0xEE9420 # ORANGE, not popped
    if player_count == 0:
        return 0xee2020 # RED, dead