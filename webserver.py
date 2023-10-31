from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

class Webserver:	
	def __init__(self, static_folder, template_folder, discord_bot):
		self.discord_bot = discord_bot
		self.static_folder = static_folder
		self.templates = Jinja2Templates(directory=template_folder)
		self.router = APIRouter()
		self.router.add_api_route("/", self.index, methods=["GET"])
		self.router.add_api_route("/get-log", self.get_log, methods=["GET"])
		self.router.add_api_route("/get-functions", self.get_functions, methods=["GET"])
		self.router.add_api_route("/static/{path:path}", self.static, methods=['GET']) 
		
	def static(self, path: str):
		path = self.static_folder + '/' + path
		try:
			return FileResponse(path)
		except FileNotFoundError:
			abort(404)

	def index(self, request: Request):
		bot_name = self.discord_bot.user
		num_guilds = len(self.discord_bot.guilds)
		context = {"request": request, "bot_name": bot_name, "num_guilds": num_guilds}
		return self.templates.TemplateResponse('index.html', context)

	def get_log(self):
		try:
			return FileResponse("logs/discord.log")
		except FileNotFoundError:
			abort(404)

	def get_functions(self, request: Request):
		return self.templates.TemplateResponse("bot-functions.html", {"request": request})
