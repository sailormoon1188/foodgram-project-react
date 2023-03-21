# Generated by Django 2.2.16 on 2023-03-19 09:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredients',
            options={'ordering': ('name',), 'verbose_name': 'Ингредиенты', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipes',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipes',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(default=0, help_text='укажите время приготовления в минутах', verbose_name='время приготовления, мин.'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(help_text='укажите нужное количество продукта', verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantity', to='recipes.Ingredients')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantity', to='recipes.Recipes')),
            ],
            options={
                'verbose_name': 'Ед.изм.',
                'verbose_name_plural': 'Ед.изм.',
            },
        ),
        migrations.AddConstraint(
            model_name='quantity',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient'),
        ),
    ]
