import datetime

from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.utils import timezone
from .fields import WEBPField
import uuid

from django.db import models
from registration.models import CustomUser

DAYS_OF_WEEK_CHOICES = [
    ('monday', 'понедельник'),
    ('tuesday', 'вторник'),
    ('wednesday', 'среда'),
    ('thursday', 'четверг'),
    ('friday', 'пятница'),
    ('saturday', 'суббота'),
    ('sunday', 'воскресенье'),
]
TECHNOLOGIES = ['Python', 'C++', 'Java', 'C#', 'Pascal']
TECHNOLOGY_CHOICES = [(tech, tech) for tech in TECHNOLOGIES]
DIFFICULTY_CHOICES = [
    ('Начинающий', 'Beginner'),
    ('Продвинутый', 'Advanced'),
]


def image_folder_Course(instance, filename):
    return 'mainpage/static/dist/img/Models/Course/CourseIcons/{}.webp'.format(uuid.uuid4().hex)


def image_folder_Technology(instance, filename):
    return 'mainpage/static/dist/img/Models/Course/TechIcons/{}.webp'.format(uuid.uuid4().hex)


class Course(models.Model):
    title = models.CharField(max_length=100)  # Тема курса
    description = models.TextField('Полное описание')  # Описание
    short_des = models.TextField('Краткое описание', default='')

    difficulty = models.CharField('Сложность курса', max_length=15, choices=DIFFICULTY_CHOICES)  # Сложность
    rating = models.DecimalField('Рейтинг курса', max_digits=3, decimal_places=1)  # Рейтинг(оценка) курса
    price = models.DecimalField('Стоимость курса', max_digits=6, decimal_places=2)  # Стоимость курса
    mentor = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE)

    start_date = models.DateField('Дата начала курса', default=timezone.now)  # Поле даты начала курса
    start_time = models.TimeField('Время начала курса', default=datetime.time(19, 0))  # Поле времени начала курса

    days_of_week = MultiSelectField('Дни недели занятий', choices=DAYS_OF_WEEK_CHOICES,

                                    validators=[MaxValueValidator(7)],
                                    default='monday')  # Чекбоксы для выбора дней недели
    technologies = MultiSelectField('Применяемы языки', choices=TECHNOLOGY_CHOICES,

                                    validators=[MaxValueValidator(5)],
                                    default='Python')  # Чекбоксы для выбора дней недели
    lessons_count = models.IntegerField(default=1)  # Кол-во уроков в курсе
    img = WEBPField(  # изображение курса
        verbose_name=('Изображение курса'),
        upload_to=image_folder_Course,
        default='mainpage/static/dist/img/Models/no_image_big.png',
    )
    tech_img = WEBPField(  # изображение языка
        verbose_name=('Изображение языка'),
        upload_to=image_folder_Technology,
        default='mainpage/static/dist/img/Models/no_image_big.png',
    )

    def save(self, *args, **kwargs):
        """Функция срабатывает при сохранении курса
        В функции происходит создание Занятий, согласно их количеству.
        При редактировании количества занятий, либо добавляются новые, либо удаляются последние.
        """
        if not self.days_of_week:
            self.days_of_week = ['wednesday', 'saturday']

        is_created = not bool(self.pk)

        super().save(*args, **kwargs)
        lesson_count = Lesson.objects.filter(course_owner_id=self.pk).count()

        if is_created:
            next_date = self.start_date
            for i in range(self.lessons_count):
                count = len(self.days_of_week)
                day = i % count

                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += datetime.timedelta(days=1)

                Lesson.objects.create(course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day], start_date=next_date.isoformat(),
                                      start_time=self.start_time)
        elif lesson_count < self.lessons_count:

            last_lesson = Lesson.objects.filter(course_owner=self).order_by('-pk').first()
            next_date = last_lesson.start_date

            for i in range(lesson_count, self.lessons_count):
                count = len(self.days_of_week)
                day = i % count
                while next_date.weekday() != self.get_weekday_index(self.days_of_week[day]):
                    next_date += datetime.timedelta(days=1)
                Lesson.objects.create(course_owner=self, mentor_owner=self.mentor,
                                      title=f'{self.title}. {self.difficulty}. Занятие {i + 1}',
                                      day_of_week=self.days_of_week[day], start_date=self.start_date,
                                      start_time=self.start_time)

        elif lesson_count > self.lessons_count:
            for i in range(self.lessons_count, lesson_count):
                last_lesson = Lesson.objects.filter(course_owner=self).order_by('-pk').first()
                if last_lesson:
                    last_lesson.delete()

    @staticmethod
    def get_weekday_index(weekday):
        return {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}[
            weekday]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course_owner = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lesson_course',
                                     null=False)  # Курс, к которому принадлежит занятие
    mentor_owner = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='lesson_mentor', null=False,

                                     default=1)  # Ментор, который проводит занятие

    title = models.CharField(max_length=255, default='Lesson 1', blank=True)  # Название занятия
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK_CHOICES, default='monday')  # день недели
    start_date = models.DateField(default=timezone.now)  # Поле даты начала занятия
    start_time = models.TimeField(default=datetime.time(19, 0))  # Поле времени начала занятия

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'


class Review(models.Model):
    owner = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='reviews', null=False)
    title = models.CharField(max_length=1000, blank=False)
    objective = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='objective', null=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
