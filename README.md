# Flask-Twisted

Simple integration of Flask and Twisted

## Installation

``` bash
pip install Flask-Twisted
```

## A Minimal Application

``` python
from flask import Flask
from flask_twisted import Twisted

app = Flask(__name__)
twisted = Twisted(app)

...

if __name__ == "__main__":
    app.run()
```

Save it as app.py (or something similar) and run it with your Python interpreter.

``` bash
python app.py
```

## A Minimal SSL Application

``` python
from flask import Flask
from flask_twisted import Twisted

app = Flask(__name__)
twisted = Twisted(app, ssl=True, ssl_cert="cert.pem", ssl_pem="key.pem")

...

if __name__ == "__main__":
    app.run()
```

Save it as ssl_app.py (or something similar) and run it with your Python interpreter.

``` bash
python ssl_app.py
```

## Twisted Daemon

``` python
from twisted.application.service import Application
from app import twisted

application = Application('twisted-flask')
twisted.run(run_reactor=False)
```

Save it as app.tac (or something similar) and run it with your Twistd program.

``` bash
twistd -ny app.tac
```

## License

This software is under the MIT license. See the complete license in:

```
LICENSE
```
