import pytest

from main import Category, Product


# Фикстура для сброса статических счётчиков перед каждым тестом
@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0


# Фикстуры для создания объектов Product
@pytest.fixture
def product_xiaomi():
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture
def product_iphone():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def product_samsung():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def product_tv():
    return Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)


# Фикстуры для создания объектов Category
@pytest.fixture
def smartphone_category(product_samsung, product_iphone):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product_samsung, product_iphone]
    )


@pytest.fixture
def tv_category(product_tv):
    return Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product_tv]
    )


# Тесты для класса Product
def test_product_initialization(product_xiaomi):
    assert product_xiaomi.name == "Xiaomi Redmi Note 11"
    assert product_xiaomi.description == "1024GB, Синий"
    assert product_xiaomi.price == 31000.0
    assert product_xiaomi.quantity == 14


def test_product_types(product_iphone):
    assert isinstance(product_iphone.name, str)
    assert isinstance(product_iphone.description, str)
    assert isinstance(product_iphone.price, float)
    assert isinstance(product_iphone.quantity, int)


# Тесты для класса Category
def test_category_initialization(smartphone_category, product_samsung, product_iphone):
    category = smartphone_category
    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )
    assert len(category.products) == 2
    assert category.products[0] is product_samsung
    assert category.products[1] is product_iphone


def test_category_counters_on_creation(smartphone_category, tv_category):
    assert Category.category_count == 2
    assert Category.product_count == 3  # 2 + 1


def test_empty_category():
    category = Category("Пустая категория", "Без товаров", [])
    assert len(category.products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


# Тесты на корректность подсчётов
def test_total_category_count(smartphone_category, tv_category):
    assert Category.category_count == 2


def test_total_product_count(smartphone_category, tv_category):
    assert Category.product_count == 3
