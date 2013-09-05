# WPUpdater

WordPress updating tool. Contains command line script (wpupdate.py) for updating WordPress via wp-admin web panel. Based on lxml html parser and xpath. 

## Requirements
Package depends on lxml library

## Configuration

Just install it by typing 
<pre>
    python setup.py install
</pre>

## Usage
Executable script should be placed in $PATH directory. 
<pre>
    wpupdate.py -l -u testuser -p testpassword www.mywordpress.com
</pre>

## TODO
* ~~Change script-look to python module~~
* Automatic plugin update
* Add more docs
* Add upgrade form customization (locale, User-agent etc.)
    
