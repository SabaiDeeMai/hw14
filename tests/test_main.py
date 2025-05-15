import pytest

from src.main import Category, Product


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


def test_modify_product_attributes(product_xiaomi):
    product_xiaomi.price = 35000.0
    product_xiaomi.quantity = 10
    assert product_xiaomi.price == 35000.0
    assert product_xiaomi.quantity == 10


def test_product_dict(product_samsung):
    product = product_samsung
    expected_dict = {
        'name': 'Samsung Galaxy S23 Ultra',
        'description': '256GB, Серый цвет, 200MP камера',
        '_price': 180000.0,
        'quantity': 5
    }
    assert product.__dict__ == expected_dict


def test_price_setter_invalid_values(caplog, product_xiaomi):
    original_price = product_xiaomi.price
    product_xiaomi.price = -100
    assert product_xiaomi.price == original_price
    assert "Цена не должна быть нулевая или отрицательная" in caplog.text

    product_xiaomi.price = 0
    assert product_xiaomi.price == original_price
    assert "Цена не должна быть нулевая или отрицательная" in caplog.text


def test_str_method(product_samsung):
    assert str(product_samsung) == "Samsung Galaxy S23 Ultra, 180000 руб. Остаток: 5 шт."


def test_new_product_classmethod():
    data = {
        "name": "Новый Телефон",
        "description": "Модель 2024 года",
        "price": 45000.0,
        "quantity": 12
    }
    product = Product.new_product(data)
    assert product.name == "Новый Телефон"
    assert product.description == "Модель 2024 года"
    assert product.price == 45000.0
    assert product.quantity == 12


# Тесты для класса Category
def test_category_initialization(smartphone_category, product_samsung, product_iphone):
    category = smartphone_category
    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )
    assert len(category._Category__products) == 2


def test_category_counters_on_creation(smartphone_category, tv_category):
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_empty_category():
    category = Category("Пустая категория", "Без товаров", [])
    assert len(category.products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_add_product_to_category(smartphone_category):
    new_product = Product("Nokia 3310", "Легендарный телефон", 1000.0, 1)
    smartphone_category.add_product(new_product)
    assert len(smartphone_category._Category__products) == 3
    assert Category.product_count == 3


def test_products_property(smartphone_category):
    expected_output = (
        "Samsung Galaxy S23 Ultra, 180000 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000 руб. Остаток: 8 шт."
    )
    assert smartphone_category.products == expected_output


def test_total_category_count(smartphone_category, tv_category):
    assert Category.category_count == 2


def test_total_product_count(smartphone_category, tv_category):
    assert Category.product_count == 3


def test_static_counter_initial_state():
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_multiple_categories():
    p1 = Product("A", "Desc A", 100, 10)
    p2 = Product("B", "Desc B", 200, 20)
    cat1 = Category("Cat1", "", [p1])
    cat2 = Category("Cat2", "", [p2])

    assert Category.category_count == 2
    assert Category.product_count == 2


def test_initial_counters():
    assert Category.category_count == 0
    assert Category.product_count == 0
