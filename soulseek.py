import json,discord,asyncio,aiohttp
from aioslsk.settings import Settings, CredentialsSettings, SharesSettings
from aioslsk.client import SoulSeekClient
from aioslsk.search.model import SearchRequest
from aioslsk.transfer.model import Transfer

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

async def list_credentials_username(path):
    slsklist = json.load(open(path+'/soulseek.json', 'r'))
    embed = discord.Embed(title="Soulseek Credentials", color=embed_color)
    i = 0
    for entry in slsklist:
        i += 1
        embed.add_field(name=str(i)+".) Username : "+entry['Username'], value='', inline=False)
    return embed

async def remove_credentials(username, password, path):
    slsklist = json.load(open(path+'/soulseek.json', 'r'))
    IsExist = False
    for entry in slsklist:
        if entry['Username'] == username and entry['Password'] == password:
            IsExist = True
            break
    if IsExist == True:
        slsklist.remove({"Username" : username, "Password" : password})          
        json.dump(slsklist, open(path+'/soulseek.json', 'w'))
        embed = discord.Embed(title="User removal successfull", color=embed_color)
        return {"status" : "success", "embed" : embed}
    else:
        embed = discord.Embed(title="User removal failed, the user does not exist or the password provided is wrong, only authorized users can remove the accounts", color=0xFF0000)
        return {"status" : "failure", "embed" : embed}

async def create_credentials(username, password, path):
    slsklist = json.load(open(path+'/soulseek.json', 'r'))
    IsExist = False
    for entry in slsklist:
        if entry['Username'] == username:
            IsExist=True
            break
    if IsExist == False:
        slsklist.append({'Username' : username, 'Password' : password})
        json.dump(slsklist, open(path+'/soulseek.json', 'w'))
        embed = discord.Embed(title='User Creation Successfull', color=embed_color)
        embed.add_field(name='Successfully added User '+username, value='', inline=False)
        return embed
    else:
        embed = discord.Embed(title='User Creation Failed', color=0xFF0000)
        embed.add_field(name='User already exists, if forget password, contact admin', value='', inline=False)
        return embed

async def search_songs(keyphrase, username, path):
    slsklist = json.load(open(path+'/soulseek.json', 'r'))
    password = None
    IsExist = False
    for entry in slsklist:
        if entry['Username'] == username:
            password = entry['Password']
            IsExist=True
            break
    if IsExist == True:
        settings: Settings = Settings(credentials=CredentialsSettings(username=username, password=password))
        client: SoulSeekClient = SoulSeekClient(settings)
        embeds = []
        await client.start()
        await client.login()
        request: SearchRequest = await client.searches.search(query=keyphrase)
        await asyncio.sleep(10)
        for result in request.results[:10]:
            embed = discord.Embed(title='Username : '+result.username, color=embed_color)
            i = 0
            for item in result.shared_items:
                i += 1
                desc = ""
                desc += "Filename : "+item.filename+"\n"
                desc += "Filesize : "+str(item.filesize)+"\n"
                desc += "Extension :"+item.extension+"\n"
                embed.add_field(name=str(i)+".)", value=desc, inline=False)
            embeds.append(embed)
        await client.stop()
        return "success",embeds
    else:
        return "failure",None

async def download_song(username, slsk_username, filename, path, message):
    slsklist = json.load(open(path+'/soulseek.json', 'r'))
    password = None
    IsExist = False
    for entry in slsklist:
        if entry['Username'] == username:
            password = entry['Password']
            IsExist=True
            break
    if IsExist == True:
        settings: Settings = Settings(credentials=CredentialsSettings(username=username, password=password), shares=SharesSettings(download=path+'/downloads'))
        client: SoulSeekClient = SoulSeekClient(settings)
        embed = discord.Embed(title="Starting Download", color=embed_color)
        reply = await message.channel.send(embed=embed)
        await client.start()
        await client.login()
        transfer: Transfer = await client.transfers.download(slsk_username, filename)
        time = 0
        while transfer.is_transfered() == False:
            time +=2
            embed = discord.Embed(title='Downloading', color=embed_color)
            embed.add_field(name='Done :-', value=str(transfer.bytes_transfered)+'/'+str(transfer.filesize), inline=False)
            await reply.edit(embed=embed)
            if time > 10 and transfer.filesize == None:
                break
            await asyncio.sleep(2)
        await client.stop()
        if time > 10 and transfer.filesize == None:
            embed = discord.Embed(title="Failure", color=0xFF0000)
            embed.add_field(name="Transfer failed, probably the user is offline", value='', inline=False)
            await reply.edit(embed=embed)
            return {"status" : "success", "desc" : "Transfer failed, But Timeout error handled successfully so its a success"}
        embed = discord.Embed(title="Uploading", color=embed_color)
        await reply.edit(embed=embed)
        url = "https://tmpfiles.org/api/v1/upload"
        file = open(transfer.local_path, "rb")
        data = aiohttp.FormData()
        data.add_field('file', file)
        res_json = None
        while True:    
            session = aiohttp.ClientSession()
            response = await session.post(url, data=data)
            res_json = await response.json()
            await session.close()
            if res_json['status'] == "success":
                break
        uploaded_url = res_json['data']['url']
        embed = discord.Embed(title="Transfer from user "+transfer.username+" completed and file uploaded to tmp file storage", color=embed_color)
        embed.add_field(name="Url", value=uploaded_url, inline=False)
        await reply.edit(embed=embed)
        return {"status" : "success", "desc" : "Transfer successfull, this message is not to de displayed"}
    else:
        return {"status" : "failure", "desc" : "User does not exist in the soulseek credentials file, please add them or retype correctly"}


