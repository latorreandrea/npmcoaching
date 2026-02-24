from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("assessments", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="TestResult"),
                migrations.DeleteModel(name="PersonalityProfile"),
                migrations.DeleteModel(name="Answer"),
                migrations.DeleteModel(name="Question"),
                migrations.DeleteModel(name="Test"),
            ],
        )
    ]
