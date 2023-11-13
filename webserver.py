from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

class Webserver:	
	def __init__(self, static_folder, template_folder, discord_bot):
		self.discord_bot = discord_bot
		self.static_folder = static_folder
		self.headers = {'Content-Language' : 'en-IN', 'X-Clacks-Overhead' : 'GNU Terry Prachet, GNU Kentaro Miura, GNU nujabes'}
		self.templates = Jinja2Templates(directory=template_folder)
		self.router = APIRouter()
		self.router.add_api_route("/", self.index, methods=["GET"])
		self.router.add_api_route("/get-discordlog", self.get_discordlog, methods=["GET"])
		self.router.add_api_route("/get-generalerrors", self.get_generalerrors, methods=['GET'])
		self.router.add_api_route("/get-helpbook", self.get_helpbook, methods=["GET"])
		self.router.add_api_route("/get-webserverlog", self.get_webserverlog, methods=["GET"])
		self.router.add_api_route("/get-sharedata", self.get_sharedata, methods=['GET'])
		self.router.add_api_route("/static/{path:path}", self.static, methods=['GET']) 
		
	def static(self, path: str):
		path = self.static_folder + '/' + path
		try:
			return FileResponse(path, headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)

	def index(self, request: Request):
		context = {"request": request}
		return self.templates.TemplateResponse('index.html', context, headers=self.headers)

	def get_discordlog(self):
		try:
			response = open("logs/discord.log", "r").read().split("\n")
			return JSONResponse(content=jsonable_encoder(response), headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)
		
	def get_generalerrors(self):
		try:
			response = open("logs/general_errors.log", "r").read().split("Traceback (most recent call last):")
			return JSONResponse(content=jsonable_encoder(response), headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)
		
	def get_helpbook(self):
		helpbook = self.discord_bot.helpbook
		try:
			return JSONResponse(content=jsonable_encoder(helpbook), headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)
		
	def get_webserverlog(self):
		try:
			response = open("logs/webserver.log", 'r').read().split("\n")
			return JSONResponse(content=jsonable_encoder(response), headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)
		
	def get_sharedata(self):
		try:
			return JSONResponse(content=jsonable_encoder(self.discord_bot.generate_share_data()), headers=self.headers)
		except FileNotFoundError:
			raise HTTPException(status_code=404, detail="Item not found", headers=self.headers)