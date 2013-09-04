# WPUpdater

Script for updating WordPress via wp-admin web panel. Based on lxml html parser and xpath. 

## Requirements
To fulfill the requirements, simply run:
<pre>
    pip install -r requirements.txt
</pre>
## Configuration
Project provides example configuration file. To configure, copy example file:
<pre>
    cp config/config.cfg.example config/config.cfg
</pre>
Open config/config.cfg and adapt to your environment.

## Usage
<pre>
    python update.py
</pre>

## TODO
* Change script-look to python module
* Automatic plugin update
* Add more docs
* Add upgrade form customization (locale, User-agent etc.)
    
