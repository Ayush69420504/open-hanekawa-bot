from aiohttp import web
import aiohttp,logging

class Server:
    def __init__(self, discord_bot, static_folder, template_folder):
        self.discord_bot = discord_bot
        self.static_folder = static_folder
        self.template_folder = template_folder
        self.headers = {'Content-Language' : 'en-IN', 'X-Clacks-Overhead' : 'GNU Terry Prachet, GNU Kentaro Miura, GNU nujabes'}
        self.routes = [web.get('/api/status', self.status), web.get('/log/discord', self.discordlog), web.get('/log/webserver', self.webserverlog),
        web.get('/log/errors', self.errors), web.get('/log/invidious', self.invidious), web.get('/', self.index), web.static(prefix='/static', path=self.static_folder)]
    
    async def start_server(self):
        app = web.Application()
        app.add_routes(self.routes)
        server_logger = logging.getLogger('aiohttp')
        server_logger.setLevel(logging.DEBUG)
        server_handler = logging.FileHandler(filename='logs/webserver.log', encoding='utf-8', mode='w')
        server_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        server_logger.addHandler(server_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner=runner, host='0.0.0.0', port=6900)
        await site.start()

    async def index(self, request):
        try:
            index = open(self.template_folder+'/index.html', 'r').read()
            return web.Response(text=index, content_type='text/html', headers=self.headers)
        except aiohttp.web_exceptions.HTTPNotFound:
            return web.Response(status=404, text="No index.html found")

    async def status(self, request):
        data = self.discord_bot.generate_share_data()
        return web.json_response(data=data, headers=self.headers)

    async def webserverlog(self, request):
        try:
            logs = open("logs/webserver.log", "r").read().split('\n')
            return web.json_response(data=logs, headers=self.headers)
        except aiohttp.web_exceptions.HTTPNotFound:
            return web.Response(status=404, text="Webserver logs not found!")
    
    async def discordlog(self, request):
        try:
            logs = open("logs/discord.log", "r").read().split('\n')
            return web.json_response(data=logs, headers=self.headers)
        except aiohttp.web_exceptions.HTTPNotFound:
            return web.Response(status=404, text="Discord logs not found!")
    
    async def errors(self, request):
        try:
            errors = open("logs/general_errors.log", "r").read().split("UUID")
            for i in range(0, len(errors)):
                errors[i] = 'UUID'+errors[i]
            return web.json_response(data=errors, headers=self.headers)
        except aiohttp.web_exceptions.HTTPNotFound:
            return web.Response(status=404, text="General Errors log not found!")

    async def invidious(self, request):
        try:
            data = open("logs/invidious.log", "r").read().split('\n')
            return web.json_response(data=data, headers=self.headers)
        except aiohttp.web_exceptions.HTTPNotFound:
            return web.Response(status=404, headers=self.headers)