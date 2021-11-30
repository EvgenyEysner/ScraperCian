from django.apps import AppConfig


class CianConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cian'

    verbose_name = 'Панель администратора'

    # нам надо переопределить метод ready,
    # чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import cian.signals
