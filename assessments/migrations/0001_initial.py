from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="Test",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("title", models.CharField(max_length=200)),
                        ("description", models.TextField(blank=True)),
                        ("is_active", models.BooleanField(default=True)),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                    ],
                    options={"ordering": ["title"], "db_table": "accounts_test"},
                ),
                migrations.CreateModel(
                    name="Question",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("text", models.CharField(max_length=500)),
                        ("order", models.PositiveIntegerField(default=1)),
                        (
                            "test",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="questions",
                                to="assessments.test",
                            ),
                        ),
                    ],
                    options={"ordering": ["order", "id"], "db_table": "accounts_question"},
                ),
                migrations.CreateModel(
                    name="Answer",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("text", models.CharField(max_length=500)),
                        ("points", models.IntegerField(default=0)),
                        ("order", models.PositiveIntegerField(default=1)),
                        (
                            "question",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="answers",
                                to="assessments.question",
                            ),
                        ),
                    ],
                    options={"ordering": ["order", "id"], "db_table": "accounts_answer"},
                ),
                migrations.CreateModel(
                    name="PersonalityProfile",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("name", models.CharField(max_length=120)),
                        ("description", models.TextField(blank=True)),
                        ("min_score", models.IntegerField()),
                        ("max_score", models.IntegerField()),
                        (
                            "test",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="personalities",
                                to="assessments.test",
                            ),
                        ),
                    ],
                    options={"ordering": ["min_score", "id"], "db_table": "accounts_personalityprofile"},
                ),
                migrations.CreateModel(
                    name="TestResult",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("score", models.IntegerField()),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        (
                            "personality",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="results",
                                to="assessments.personalityprofile",
                            ),
                        ),
                        (
                            "test",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="results",
                                to="assessments.test",
                            ),
                        ),
                        (
                            "user",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="test_results",
                                to=settings.AUTH_USER_MODEL,
                            ),
                        ),
                    ],
                    options={"ordering": ["-created_at"], "db_table": "accounts_testresult"},
                ),
            ],
        )
    ]
