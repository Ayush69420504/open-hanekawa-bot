function refreshlog() {
	request = new XMLHttpRequest()
	request.open('GET', '/get-log', true)
	request.responseType = 'text'
	request.send(null)
	request.onload = function() {
		ele = document.getElementById('log')
		ele.innerHTML = '<ul>'
		logs = request.responseText.split('\n')
		for (i = 0; i < logs.length; i++)
		{
			ele.innerHTML += '<li>' + logs[i] + '</li>'
		}
		ele.innerHTML += '</ul>'
	}
}
