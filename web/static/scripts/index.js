async function refreshlog() {
	//Refreshes the discord logs
	response = await fetch("/get-discordlog")
	logs = await response.json()
	log_container = document.getElementById("discord-logs")
	i = 0
	for (log of logs)
	{
		log_container.innerHTML += '<div class="discord-log-message">'+i+'. '+log+'</div>'
		i++
	}
	log_container.scrollTo(0, log_container.scrollHeight)
}
async function refreshErrors() {
	//Refreshes general_errors
	response = await fetch("/get-generalerrors")
	errors = await response.json()
	error_container = document.getElementById("general-errors")
	i = 0
	for (error of errors)
	{
		error_container.innerHTML += '<div class="general-error-message">'+i+'. '+error+'</div>'
		i++
	}
	error_container.scrollTo(0, error_container.scrollHeight)
}
async function render_helpbook() {
	//Loads the helpbook
	response = await fetch("/get-helpbook")
	helpbook = await response.json()
	helpbook_container = document.getElementById("functions")
	keys = Object.keys(helpbook)
	i = 1
	for (key of keys)
	{
		h3 = '<h3> '+i+'. '+key+'</h3>'
		doc = '<p>'+helpbook[key]+'</p>'
		helpbook_container.innerHTML += '<div id=help_entry_'+i+'>'+h3+doc+'</div>'
		i++
	}
}
async function render_sharedata() {
	//Loads share data
	response = await fetch("/get-sharedata")
	sharedata = await response.json()
	sharedata_container = document.getElementById("sharedata")
	sharedata_container.innerHTML += "<h2>Logged in as "+sharedata['bot_name']+"</h2>"
	sharedata_container.innerHTML += "<h2>Currently serving "+sharedata['num_guilds']+" guilds</h2>"
	sharedata_container.innerHTML += "<h2>Has "+sharedata['num_functions']+" functions</h2>"
	sharedata_container.innerHTML += "<h2>Working Directory : "+sharedata['workdir']+"</h2>"
}
async function start() {
	await render_sharedata()
	await render_helpbook()
	await refreshlog()
	await refreshErrors()
}