# Generated by Django 2.2.16 on 2023-04-21 16:30

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='укажите нужное количество продукта', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'ингредиены с ед.измерения',
                'verbose_name_plural': 'сводная таблица с ед.изм.',
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='укажите название рецепта', max_length=200, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('image', models.ImageField(blank=True, upload_to='recipes/', verbose_name='Картинка')),
                ('cooking_time', models.PositiveSmallIntegerField(default=0, help_text='укажите время приготовления в минутах', verbose_name='время приготовления, мин.')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название тега')),
                ('slug', models.SlugField(unique=True, verbose_name='слаг для тега')),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(code='invalid_color', message='HEX-код цвета должен быть в формате #RRGGBB или #RGB', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')], verbose_name='цвет тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.AlterModelOptions(
            name='ingredients',
            options={'ordering': ('name',), 'verbose_name': 'Ингредиенты', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.RenameField(
            model_name='ingredients',
            old_name='unit',
            new_name='measurement_unit',
        ),
        migrations.AlterField(
            model_name='ingredients',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор, на которого подписка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.Recipes', verbose_name='Рецепт в список покупок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Список покупок',
            },
        ),
        migrations.CreateModel(
            name='RecipeTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tags', to='recipes.Recipes')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tags', to='recipes.Tags')),
            ],
        ),
        migrations.AddField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингредиенты', through='recipes.IngredientInRecipe', to='recipes.Ingredients', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipes',
            name='tags',
            field=models.ManyToManyField(help_text='Теги к рецептам', through='recipes.RecipeTags', to='recipes.Tags', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientinrecipe', to='recipes.Ingredients', verbose_name='ингредиент'),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientinrecipe', to='recipes.Recipes'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.Recipes', verbose_name='Рецепт в избранном')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='subscriptions',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_subscriptions'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='recipetags',
            constraint=models.UniqueConstraint(fields=('recipe', 'tag'), name='recipe_tag_unique'),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
