from app.Application import Application
from app.Drawing import DrawingFactory

factories = {'drawing': DrawingFactory}

app = Application(factories)
app.run()
