from django.db import models


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-completion_date')

    def get_date_range(self, date_1, date_2):
        return super().get_queryset().filter(completion_date__range=(date_1, date_2))

class Technician(models.Model):
    name = models.CharField('ФИО техника', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Техник"
        verbose_name_plural = "Техники"

class ApplicationObject(models.Model):
    number_object = models.BigIntegerField('Номер объекта')
    URGENCY = (
        ('Без сроков', 'Без сроков'),
        ('!!!', '!!!'),
        ('Срочно', 'Срочно'),
        ('На согласование', 'На согласование'),
        ('Согласовано', 'Согласовано'),
    )
    urgency_application = models.CharField('Срочность заявки', max_length=30, choices=URGENCY, default='Без сроков')
    date_application = models.DateTimeField('Дата создания заявки', editable=True, auto_now_add=True)
    name_object = models.CharField('Имя объекта', max_length= 128)
    address_object = models.CharField('Адрес', max_length=128)
    ZONE = (
        ('Северо-Запад', 'Северо-Запад'),
        ('Центр', 'Центр'),
        ('Область', 'Область'),
        ('Обслуживание', 'Обслуживание'),
        ('АМЗ', 'АМЗ'),
        ('ЧТЗ', 'ЧТЗ'),
        ('ЧМЗ', 'ЧМЗ'),
        ('Ленинский','Ленинский'),
        ('Сосновский','Сосновский'),
        ('Екб. + Свердловская область', 'Екб. + Свердловская область')
    )
    service_area = models.CharField('Район', max_length=70, choices=ZONE, default='Область')
    PROBLEM = (
        ('Сработка шлейф', 'Сработка шлейф'),
        ('Присвоить / удалить код', 'Присвоить / удалить код'),
        ('Не проходит постановка / снятие', 'Не проходит постановка / снятие'),
        ('Проверка оборудования', 'Проверка оборудования'),
        ('Отсутствие а/т', 'Отсутствие а/т'),
        ('Cработка ПС', 'Cработка ПС'),
        ('Разряд АКБ', 'Разряд АКБ'),
        ('Ложное КТС', 'Ложное КТС'),
        ('Уточнить расшлейфовку', 'Уточнить расшлейфовку'),
        ('Видеонаблюдение', 'Видеонаблюдение'),
        ('Демонтаж оборудования', 'Демонтаж оборудования'),
        ('Инструктаж пользователей', 'Инструктаж пользователей'),
        ('Осмотр ТСО', 'Осмотр ТСО'),
        ('Отсутсвие 220', 'Отсутсвие 220'),
        ('Переключение', 'Переключение'),
        ('Уточнение Сим карт', 'Уточнение Сим карт'),
        ('Двойник', 'Двойник'),
        ('Подключить ТРС', 'Подключить ТРС'),
        ('Обслуживание ПС', 'Обслуживание ПС'),
        ('Сверка пользователей', 'Сверка пользователей'),
        ('Корректировка настроек', 'Корректировка настроек'),
        ('Доблокировка', 'Доблокировка'),
    )
    type_of_problem = models.CharField('Тип проблемы', max_length=120, choices=PROBLEM, default='Сработка шлейф')
    comment = models.TextField('Комментарий')
    completion_date = models.DateField('Дата для заявки')
    INITIATOR = (
        ('Ответственный', 'Ответственный'),
        ('Менеджер', 'Менеджер'),
        ('ГБР', 'ГБР'),
        ('Офис', 'Офис'),
        ('Письмо', 'Письмо'),
        ('Оператор', 'Оператор'),
        ('Техник', 'Техник'),
        ('Монтажники', 'Монтажники'),
    )
    source_application = models.CharField('Инициатор', max_length=20, choices=INITIATOR, default='Менеджер')
    initiator_of_the_application = models.CharField('Имя инициатора', max_length=128)
    STATUS = (
        ('Закрыта', 'Закрыта'),
        ('В работе', 'В работе'),
    )
    status_application = models.CharField('Статус заявки', max_length=20, choices=STATUS, default='В работе')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Номер объекта %s от %s" % (self.number_object, self.completion_date)

    def get_absolute_url(self):
        return f'/about/{self.id}'

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    objects = models.Manager()
    custom_manager = CustomManager()

