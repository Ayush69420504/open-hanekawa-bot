import subprocess

#Uses 0x0.st a null pointer website to upload images and store it in web
#Personally i set the expiry timeout to 900 seconds of current time
#That is in accordance with fair use of the site and not to saturate it completely :)
#I copied this code from a russian guy's blog, could have written it myself
#But i am too lazy for that ;)

def upload_file_url(url, expires=None, secret=None):
    if expires == None:
        if secret == None:
            command = f"curl -F'url={url}' https://0x0.st"
        else:
            command = f"curl -F'url={url}' -Fsecret=https://0x0.st"
    else:
        if secret == None:
            command = f"curl -F'url={url}' -Fexpires={expires} https://0x0.st"
        else:
            command = f"curl -F'url={url}' -Fexpires={expires} -Fsecret=https://0x0.st"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error from upload_file_url:\n {e}"

def delete_file(token, url):
    command = f"curl -Ftoken={token} -Fdelete={url}"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error from delete_file:\n {e}"

def change_expires(url, expires, token):
    command = f"curl -Ftoken={token} -Fexpires={expires} {url}"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error from change_expires:\n {e}"
    
def upload_file_path(path, expires=None, secret=None):
    if expires == None:
        if secret == None:
            command = f"curl -F'file=@{path}' https://0x0.st"
        else:
            command = f"curl -F'file=@{path}' -Fsecret=https://0x0.st"
    else:
        if secret == None:
            command = f"curl -F'file=@{path}' -Fexpires={expires} https://0x0.st"
        else:
            command = f"curl -F'file=@{path}' -Fexpires={expires} -Fsecret=https://0x0.st"
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"Error from upload_file_path:\n {e}"
