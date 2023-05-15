import pyvirtualdisplay
import selenium
import selenium.webdriver
import time
import base64
import json

root_url = 'https://www.google.com'
download_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'

print('Opening virtual display')
display = pyvirtualdisplay.Display(visible=0, size=(1280, 1024,))
display.start()
print('\tDone')

print('Opening web browser')
driver = selenium.webdriver.Firefox()
#driver = selenium.webdriver.Chrome() # Alternately, give Chrome a try
print('\tDone')

print('Retrieving initial web page')
driver.get(root_url)
print('\tDone')

print('Injecting retrieval code into web page')
driver.execute_script("""
    window.file_contents = null;
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.onload = function() {
        var reader  = new FileReader();
        reader.onloadend = function() {
            window.file_contents = reader.result;
        };
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', %(download_url)s);
    xhr.send();
""".replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ') % {
    'download_url': json.dumps(download_url),
})

print('Looping until file is retrieved')
downloaded_file = None
while downloaded_file is None:
    # Returns the file retrieved base64 encoded (perfect for downloading binary)
    downloaded_file = driver.execute_script('return (window.file_contents !== null ? window.file_contents.split(\',\')[1] : null);')
    print(downloaded_file)
    if not downloaded_file:
        print('\tNot downloaded, waiting...')
        time.sleep(0.5)
print('\tDone')

print('Writing file to disk')
fp = open('google-logo.png', 'wb')
fp.write(base64.b64decode(downloaded_file))
fp.close()
print('\tDone')
driver.close() # close web browser, or it'll persist after python exits.
display.popen.kill() # close virtual display, or it'll persist after python exits.