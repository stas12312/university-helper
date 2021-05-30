import datetime
import random
import time
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4 import element
from fastapi import HTTPException
from sqlalchemy import insert, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app import models
from app import services
from app.core.celery_app import get_asnwers


@dataclass
class Question:
    id: int
    rubric: str
    text: str
    answers: list[str]
    type: Optional[int] = None


@dataclass
class Test:
    id: int
    title: str
    questions: list[Question]


class ParseTestService:

    @classmethod
    def get_soup_from_uri(cls, uri: str) -> BeautifulSoup:
        """Получение объетка для парсинга с URI"""
        page = requests.get(uri).content.decode()
        return BeautifulSoup(page, 'html.parser')

    @classmethod
    def get_questions(cls, soup: BeautifulSoup) -> list[element.Tag]:
        """Получение вопросов"""
        return soup.findAll('div', {'class': 'question_blocks_'})

    @classmethod
    def get_rubrics(cls, soup: BeautifulSoup) -> list[element.Tag]:
        """Получение рубрик вопросов"""
        return soup.findAll('div', {'class': 'rubric-block'})

    @classmethod
    def get_corrected_answers(cls, question: element.Tag, question_id: int) -> tuple[list[str], int]:
        """Получение правильного ответа для вопроса"""
        labels: list[element.Tag] = question.findAll('label')
        corrected_asnwers = []
        question_type = 0
        if labels:
            for j, label_ in enumerate(labels):
                input_ = label_.findAll('input')[0]
                if input_['type'] in ['checkbox', 'radio'] and input_['corrected'] == '1':
                    corrected_asnwers.append(label_.findAll('span')[0].text.strip())
                    question_type = 1
                elif input_['type'] == 'text':
                    corrected_asnwers.append(input_['corrected'])
                    question_type = 2
        else:
            pairs = question.findAll('input', {'class': f'correct_response_pair_{question_id}'})
            for pair in pairs:
                from_, to_ = pair['value'].split(' ')
                from_soup = question.findAll('div', {'id': f'row_id_{from_}_{question_id}'})
                to_soup = question.findAll('div', {'col_id': f'{to_}'})
                corrected_asnwers.append(f'{from_soup[0].text} => {to_soup[0].text}')
            question_type = 3
        return corrected_asnwers, question_type

    @classmethod
    def save_questions_in_file(cls, questions: list[Question], filename: str) -> None:
        """Сохранение вопросов в файл"""
        with open(filename, 'w+', encoding='utf-8') as f:
            for question in questions:
                f.write(f'Вопрос {question.id}: {question.rubric}'
                        f'{question.text}'
                        f'Ответы: {question.answers}\n\n')

    @classmethod
    def get_answers(cls, uri: str, min_iterations: int = 10, accept_repeats: int = 3) -> list[Question]:
        """Получение правильных ответов"""
        question_ids = set()
        questions = []
        accept_repeats_ = 0
        i = 0
        questions_count = 0
        while i < 10 or accept_repeats_ < accept_repeats:
            time.sleep(random.randint(21, 41))
            soup = cls.get_soup_from_uri(uri)
            soup_questions = cls.get_questions(soup)
            soup_rubrics = cls.get_rubrics(soup)
            for j in range(len(soup_questions)):
                soup_question = soup_questions[j]
                question_id = int(soup_question['id'].split('_')[-1])
                if question_id in question_ids:
                    continue
                prev_block = soup_question.find_previous_sibling('div')
                rubrick = None
                if prev_block is not None and 'rubric-block' in prev_block['class']:
                    rubrick = prev_block.text
                question_ids.add(question_id)
                text_question = soup_question.findAll('div')[0].text.strip()
                # question_type = soup_rubrics[i].findAll('p')[0].text.strip()
                corrected_asnwers, question_type = cls.get_corrected_answers(soup_question, question_id)

                questions.append(Question(question_id, rubrick, text_question, corrected_asnwers, question_type))
            # Проверяем, что были получены новые вопросы
            print(f'{questions_count}, {len(questions)}, {len(questions) - questions_count}')
            if questions_count == len(questions):
                accept_repeats_ += 1
            else:
                questions_count = len(questions)
                accept_repeats_ = 0
            i += 1
            print(f'{accept_repeats_}, {i}\n')

        return questions

    @classmethod
    def get_test_with_answers(cls, test_id: int) -> Optional[Test]:
        uri = f'https://dispace.edu.nstu.ru/ditest/index/offline/html/{test_id}'
        soup = cls.get_soup_from_uri(uri)
        title_block = soup.find('span', {'id': 'tname'})
        if not title_block:
            return None
        title = title_block.text
        answers = cls.get_answers(uri, 10)

        return Test(
            id=test_id,
            title=title,
            questions=answers,

        )

    @classmethod
    def get_test(cls, test_id: int) -> Optional[Test]:
        """Получение теста"""
        uri = f'https://dispace.edu.nstu.ru/ditest/index/offline/html/{test_id}'

        test = cls.get_test_with_answers(test_id)
        if not test:
            return None

        test.questions = sorted(test.questions, key=lambda x: x.id)
        questions_data = []
        for question in test.questions:
            questions_data.append(Question(**{
                'id': question.id,
                'rubric': question.rubric,
                'text': question.text,
                'answers': question.answers
            }))
        test = {
            'id': test.id,
            'title': test.title,
            'questions': questions_data,
        }
        return Test(**test)


class TestService:

    @classmethod
    async def create(cls, db: AsyncSession, user: models.User, test_id: int) -> models.Test:
        """Создание нового теста"""

        c_date = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=10)
        # Проверка, что прошло 10 минут с последнего заказа
        if not user.is_superuser:
            result = await db.execute(
                select(models.Test).where(models.Test.user_id == user.id, models.Test.created_at >= c_date)
            )
            if result.scalars().first():
                raise HTTPException(status_code=400, detail='Делать заказ можно не чаще, чем раз в 10 минут')

        result = await db.execute(
            insert(models.Test)
                .values(user_id=user.id, external_id=test_id, created_at=datetime.datetime.now())
                .returning(models.Test.uuid)
        )
        await db.commit()
        test_uuid: str = result.scalars().first()

        get_asnwers.delay(test_uuid)

        result = await db.execute(select(models.Test).where(models.Test.uuid == test_uuid))

        return result.scalar_one()

    @classmethod
    async def get(cls, db: AsyncSession, user: models.User, test_uuid: str) -> models.Test:
        """Получение теста для пользователя"""
        result = await db.execute(
            select(models.Test)
                .where(models.Test.uuid == test_uuid)
                .options(joinedload(models.Test.questions))
        )
        test: models.Test = result.scalars().first()
        if not test:
            raise HTTPException(status_code=404, detail='Тест не найден')
        if test.user_id != user.id:
            raise HTTPException(status_code=403, detail='Нет доступа')
        return test

    @classmethod
    async def get_all_for_user(cls, db: AsyncSession, user: models.User) -> list[models.Test]:
        """Получение списка тестов для пользователя"""
        result = await db.execute(
            select(models.Test).where(models.Test.user_id == user.id).order_by(desc(models.Test.created_at)))
        return result.scalars().all()

    @classmethod
    async def get_questions(cls, db: AsyncSession, user: models.User, test_uuid: str) -> list[models.Question]:
        """Получение вопросов теста"""
        test = await cls.get(db, user, test_uuid)
        if not test.is_paid:
            raise HTTPException(status_code=400, detail='Для получение вопросов требуется оплата')
        return test.questions

    @classmethod
    async def pay_test(cls, db: AsyncSession, user: models.User, test_uuid: str) -> Test:
        """Оплата теста"""
        test = await cls.get(db, user, test_uuid)
        if test.is_paid:
            raise HTTPException(status_code=400, detail='Тест оплачен')

        pay = await services.PayServce.add_pay(db, 1, f'Оплата тесте #{test.uuid}', test.cost, user.id)
        test.pay_uuid = pay.uuid
        test.is_paid = True
        await db.commit()
        return test
