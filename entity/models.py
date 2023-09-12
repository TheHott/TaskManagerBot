from peewee import Model, TextField, ForeignKeyField, BigIntegerField, TimeField, DateField, \
    IntegerField, PostgresqlDatabase

import config
from entity.statuses import TaskStatus

db_params = config.get_db_params()
print(db_params['host'])
print(type(db_params['host']))
database = PostgresqlDatabase(db_params['name'],
                              host=db_params['host'],
                              user=db_params['user'],
                              password=db_params['password'])


class BaseModel(Model):
    class Meta:
        database = database


class Role(BaseModel):
    name = TextField(column_name='name', null=False)


class User(BaseModel):

    telegram_id = BigIntegerField(null=False)
    role_id = ForeignKeyField(Role, backref='users')
    name = TextField(column_name='name')


class Task(BaseModel):
    user_id = ForeignKeyField(User, backref='tasks')
    text = TextField(column_name='text', null=True)
    description = TextField(column_name='description', null=True)
    date = DateField(null=True)
    time = TimeField(null=True)
    status = IntegerField(null=True, default=TaskStatus.DRAFT.value)

    TASK_COMPLETE_ICON = '🟢'
    TASK_ACTIVE_ICON = '🔴'
    TASK_DRAFT_ICON = '✍'
    TASK_DELETED_ICON = '🗑'

    def as_short_str(self):
        short_str = self.get_status_as_icon()
        if self.text is None:
            short_str += " Название не указано"
        else:
            short_str += " " + self.text

        if self.date is None:
            short_str += ' (Дата не указана, '
        else:
            short_str += ' (' + self.date.strftime('%d %B %Y') + ','

        if self.time is None:
            short_str += ' Время не указано)'
        else:
            short_str += ' ' + str(self.time) + ')'

        return short_str

    def get_status_as_icon(self):
        if self.status == TaskStatus.DRAFT.value:
            return self.TASK_DRAFT_ICON
        elif self.status == TaskStatus.ACTIVE.value:
            return self.TASK_ACTIVE_ICON
        elif self.status == TaskStatus.DELETED.value:
            return self.TASK_DELETED_ICON
        elif self.status == TaskStatus.COMPLETED.value:
            return self.TASK_COMPLETE_ICON
        return ''

    def get_task_as_message(self):
        message_text = "ℹ️ "
        if self.text is None:
            message_text += "<b>Название не указано</b>\n"
        else:
            message_text += "<b>" + self.text + "</b>\n"

        if self.description is None:
            message_text += 'Описание не указано\n'
        else:
            message_text += self.description + '\n'
        message_text += '______________________________________________________\n'

        if self.date is None:
            message_text += '📅 <b>Дата:</b> не указана; '
        else:
            message_text += '📅 <b>Дата:</b> ' + str(self.date) + '; '

        if self.time is None:
            message_text += '⏱ <b>Время:</b> не указано\n'
        else:
            message_text += '⏱ <b>Время:</b> ' + str(self.time) + '\n'

        if self.status == TaskStatus.DRAFT.value:
            message_text += self.get_status_as_icon() + ' <b>Черновик</b>'
        elif self.status == TaskStatus.ACTIVE.value:
            message_text += self.get_status_as_icon() + ' <b>Не выполнена</b>'
        elif self.status == TaskStatus.DELETED.value:
            message_text += self.get_status_as_icon() + ' <b>Удалена</b>'
        elif self.status == TaskStatus.COMPLETED.value:
            message_text += self.get_status_as_icon() + ' <b>Выполнена</b>'
        else:
            message_text += '<b>Неизвестный статус</b>'

        return message_text
