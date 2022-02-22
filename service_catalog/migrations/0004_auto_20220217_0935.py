# Generated by Django 3.2.12 on 2022-02-17 08:35

from django.db import migrations, models
import django.db.models.deletion


def migrate_json_to_tower_survey_field(apps, schema_editor):
    Operation = apps.get_model('service_catalog', 'Operation')
    from service_catalog.models.tower_survey_field import TowerSurveyField
    for operation in Operation.objects.all():
        for field_name, enabled in operation.enabled_survey_fields.items():
            TowerSurveyField.objects.create(name=field_name, enabled=enabled, operation_id=operation.id)


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0003_auto_20220202_1602'),
    ]

    operations = [

        migrations.CreateModel(
            name='TowerSurveyField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Field name')),
                ('enabled', models.BooleanField(default=True)),
                ('default', models.CharField(blank=True, max_length=200, null=True, verbose_name='Default value')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tower_survey_fields', related_query_name='tower_survey_field', to='service_catalog.operation')),
            ],
            options={
                'unique_together': {('operation', 'name')},
            },
        ),
        migrations.RunPython(migrate_json_to_tower_survey_field),
        migrations.RemoveField(
            model_name='operation',
            name='enabled_survey_fields',
        ),

    ]