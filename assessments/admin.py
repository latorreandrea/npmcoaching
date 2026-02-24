from django.contrib import admin

from .models import Answer, PersonalityProfile, Question, Test, TestResult


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PersonalityProfileInline(admin.TabularInline):
    model = PersonalityProfile
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    inlines = [QuestionInline, PersonalityProfileInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "test", "order")
    list_filter = ("test",)
    search_fields = ("text", "test__title")
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "points", "order")
    list_filter = ("question__test",)
    search_fields = ("text", "question__text")


@admin.register(PersonalityProfile)
class PersonalityProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "test", "min_score", "max_score")
    list_filter = ("test",)
    search_fields = ("name", "test__title")


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "score", "personality", "created_at")
    list_filter = ("test", "personality")
    search_fields = ("user__email", "test__title")
    readonly_fields = ("created_at",)
