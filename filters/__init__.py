from .via_bot import ViaBot
from loader import dispatcher

if __name__ == "filters":
    dispatcher.filters_factory.bind(ViaBot)
