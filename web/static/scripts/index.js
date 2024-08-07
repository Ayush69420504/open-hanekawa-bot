async function refreshlog() {
	//Refreshes the discord logs
	response = await fetch("/log/discord")
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
	response = await fetch("/log/errors")
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
async function render_status() {
	//Loads the helpbook and sharedata from the status endpoint
	response = await fetch("/api/status")
	data = await response.json()
	sharedata_container = document.getElementById("sharedata")
	sharedata_container.innerHTML += "<h2>Logged in as "+data["bot_name"]+"</h2>"
	sharedata_container.innerHTML += "<h2>Using ego "+data["bot_ego"]+"</h2>"
	sharedata_container.innerHTML += '<h2>Currently serving '+data['num_guilds']+' guilds</h2>'
	sharedata_container.innerHTML += "<h2>Has "+data['num_functions']+" functions</h2>"
	sharedata_container.innerHTML += "<h2>Working Directory : "+data['workdir']+"</h2>"
	helpbook = data['helpbook']
	helpbook_container = document.getElementById("functions")
	helpbook_container.innerHTML += "<h3>Syntax: "+data['ego_prefix']+" (command) (data, data, ...) //data is seperated by spaces</h3>"
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
async function start() {
	await render_status()
	await refreshlog()
	await refreshErrors()
}