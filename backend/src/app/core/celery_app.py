import asyncio

from celery import Celery
from sqlalchemy import insert
from sqlalchemy.orm import joinedload

from app import models
from app.db.session import db_session

celery = Celery("worker", broker="redis://redis:6379")

celery.conf.task_routes = {"app.worker.celery": "main-queue"}


class SqlAlchemyTask(celery.Task):
    """An abstract Celery Task that ensures that the connection the the
    database is closed on task completion"""
    abstract = True

    # noinspection PyMethodMayBeStatic
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@celery.task(name='get_answers', base=SqlAlchemyTask)
def get_asnwers(test_uuid: str):
    from app.services.tests import ParseTestService
    from app.services.email import EmailService
    test: models.Test = db_session \
        .query(models.Test).filter(models.Test.uuid == test_uuid) \
        .options(joinedload(models.Test.user)).one()

    test.status = models.Test.IN_PROCESS
    db_session.add(test)
    db_session.commit()

    # Получение тестового теста
    if test.external_id == 1:
        test.title = 'Тест для проверки'
        test.cost = 1

        db_questions = [
            {
                'external_id': 1,
                'type': 0,
                'test_id': test.uuid,
                'rubric': 'Выбор правильного ответа',
                'body': 'Выберите правильный ответ',
                'answers': ['Правильный ответ']
            },
            {
                'external_id': 2,
                'type': 0,
                'test_id': test.uuid,
                'rubric': 'Введите правильный ответ',
                'body': 'Сколько будет 12+12',
                'answers': ['24']
            },
            {
                'external_id': 3,
                'type': 0,
                'test_id': test.uuid,
                'rubric': 'Соотнесите понятия',
                'body': '',
                'answers': ['Первое понятие => Правильный ответ 1', 'Второе понятие => Правильный ответ 2']
            },
        ]
    else:
        test_data = ParseTestService.get_test(test.external_id)
        if not test_data:
            test.status = models.Test.ERROR
            db_session.add(test)
            db_session.commit()
            asyncio.run(
                EmailService.send_notification_about_error_test(test.user.email, test.external_id)
            )
            return
        question_count = len(test_data.questions)
        cost = 7
        if question_count >= 201:
            cost = 1
        if question_count >= 151:
            cost = 2
        if question_count >= 101:
            cost = 3
        if question_count >= 76:
            cost = 4
        if question_count >= 51:
            cost = 5
        if question_count >= 26:
            cost = 6

        test.title = test_data.title
        test.cost = cost * question_count
        test.status = models.Test.SUCCESS
        db_session.add(test)

        db_questions = []
        for question in test_data.questions:
            db_questions.append({
                'external_id': question.id,
                'type': 0,
                'test_id': test.uuid,
                'rubric': question.rubric,
                'body': question.text,
                'answers': question.answers,
            })

    db_session.execute(insert(models.Question).values(db_questions))
    db_session.commit()
    asyncio.run(
        EmailService.send_notification_about_test(test.user.email, test.uuid, test.title, test.external_id))
