from controllers.Strategy import Context
from controllers.Arduino import Arduino
from controllers.Copelia import Copelia

interface = Context(Arduino())

# Para mudar o tipo de conexao
interface.strategy = Copelia()