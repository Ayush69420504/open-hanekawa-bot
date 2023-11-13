import requests,discord,json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
#embed_gen contains template functions to generate embeds
from utils import embed_gen
from PIL import Image
from io import BytesIO

defaults = json.load(open('defaults.json', 'r'))
embed_color = int(defaults['embed_color'], 0)

def search_manga(keyword):	
	embeds = []
	url = 'https://manganato.com/search/story/'+keyword
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html5lib')
	manga_list = soup.findAll('div', attrs={'class':'search-story-item'})
	for manga in manga_list:
		title = manga.h3.a['title']
		manga_code = manga.h3.a['href']
		manga_code = manga_code[manga_code.rindex('/')+1:]		
		latest_chapter = manga.findAll('a', attrs={'class':'item-chapter a-h text-nowrap'})[0].string
		author_name = manga.findAll('span', attrs={'class':'text-nowrap item-author'})[0]['title']	
		imurl = manga.img['src']
		embeds.append(embed_gen.search_manga(title, manga_code, latest_chapter, author_name, imurl))
	return embeds

def list_chapters(keyword, start, end):
	embeds = []
	url = 'https://chapmanganato.com/'+keyword
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html5lib')
	chapter_list = soup.findAll('li', attrs={'class':'a-h'})
	chapter_list.reverse()
	i = 0
	start_index = 0
	end_index = len(chapter_list)
	for chapters in chapter_list:
		chap_num = chapters.a['href']
		chap_num = chap_num[chap_num.rindex('/')+1:]
		if start != None and chap_num == 'chapter-'+str(start):
			start_index = i
		elif end != None and chap_num == 'chapter-'+str(end):
			end_index = i
			break
		i += 1
	chapter_list = chapter_list[start_index:end_index+1]
	intervals = len(chapter_list)//10
	for i in range(0, intervals):
		embed = discord.Embed(color=embed_color)
		for chapters in chapter_list[10*i:10*(i+1)]:
			chap_num = chapters.a['href']
			chap_num = chap_num[chap_num.rindex('/')+1:]
			embed.add_field(name=chap_num, value='\n', inline=False)
		embeds.append(embed)
	embed = discord.Embed(color=embed_color)
	for chapters in chapter_list[intervals*10:len(chapter_list)]:
		chap_num = chapters.a['href']
		chap_num = chap_num[chap_num.rindex('/')+1:]
		embed.add_field(name=chap_num, value='\n', inline=False)
	embeds.append(embed)
	return embeds

