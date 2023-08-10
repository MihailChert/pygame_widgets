from app.Application import Application, Builder
from app.Drawing import DrawingFactory

factories = {'drawing': DrawingFactory}
builder = Builder.build_from('defaultappconfig.json')
app = Application.create_from_builder(builder)
app.run()
