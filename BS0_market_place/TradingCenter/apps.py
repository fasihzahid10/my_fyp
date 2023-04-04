from django.apps import AppConfig


class TradingcenterConfig(AppConfig):
    name = 'TradingCenter'
    def ready(self):
        import TradingCenter.mysignal