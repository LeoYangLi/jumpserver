# Generated by Django 4.1.13 on 2024-09-06 08:32

from django.conf import settings
from django.db import migrations, models
from orgs.models import Organization


def migrate_ops_adhoc_and_playbook_name(apps, schema_editor):
    Adhoc = apps.get_model('ops', 'adhoc')
    Playbook = apps.get_model('ops', 'playbook')
    Organization = apps.get_model('orgs', 'Organization')
    org_id_name_mapper = {str(org.id): org.name for org in Organization.objects.all()}

    adhocs_to_update = Adhoc.objects.exclude(org_id=Organization.DEFAULT_ID)
    for adhoc in adhocs_to_update:
        suffix = org_id_name_mapper.get(str(adhoc.org_id), str(adhoc.id)[:6])
        adhoc.name = f'{adhoc.name} ({suffix})'
    Adhoc.objects.bulk_update(adhocs_to_update, ['name'])

    playbooks_to_update = Playbook.objects.exclude(org_id=Organization.DEFAULT_ID)
    for playbook in playbooks_to_update:
        suffix = org_id_name_mapper.get(str(playbook.org_id), str(playbook.id)[:6])
        playbook.name = f'{playbook.name} ({suffix})'
    Playbook.objects.bulk_update(playbooks_to_update, ['name'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ops', '0002_celerytask'),
        ('orgs', '0002_auto_20180903_1132'),
    ]

    operations = [
        migrations.RunPython(migrate_ops_adhoc_and_playbook_name),
        migrations.AlterUniqueTogether(
            name='adhoc',
            unique_together={('name', 'creator')},
        ),
        migrations.AlterUniqueTogether(
            name='playbook',
            unique_together={('name', 'creator')},
        ),
        migrations.AddField(
            model_name='adhoc',
            name='scope',
            field=models.CharField(default='public', max_length=64, verbose_name='Scope'),
        ),
        migrations.AddField(
            model_name='playbook',
            name='scope',
            field=models.CharField(default='public', max_length=64, verbose_name='Scope'),
        ),
        migrations.RemoveField(
            model_name='adhoc',
            name='org_id',
        ),
        migrations.RemoveField(
            model_name='playbook',
            name='org_id',
        ),
    ]