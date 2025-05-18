import pytest
from src.main import Product, Category


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
        'price': 180000.0,
        'quantity': 5
    }
    assert product.__dict__ == expected_dict


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
    # Смартфоны: 5 + 8 = 13 шт.
    # Телевизоры: 7 шт.
    assert Category.category_count == 2
    assert Category.product_count == 13 + 7  # 20 шт.


def test_empty_category():
    category = Category("Пустая категория", "Без товаров", [])
    assert len(category.products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_add_product_to_category(smartphone_category):
    new_product = Product("Nokia 3310", "Легендарный телефон", 1000.0, 1)
    smartphone_category.products.append(new_product)
    Category.product_count += new_product.quantity  # Ручное обновление счётчика (лучше через add_product)

    assert len(smartphone_category.products) == 3
    assert Category.product_count == 5 + 8 + 1  # 14 шт.


def test_total_category_count(smartphone_category, tv_category):
    assert Category.category_count == 2


def test_total_product_count(smartphone_category, tv_category):
    assert Category.product_count == 5 + 8 + 7  # 20 шт.


def test_static_counter_initial_state():
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_multiple_categories():
    p1 = Product("A", "Desc A", 100, 10)
    p2 = Product("B", "Desc B", 200, 20)
    cat1 = Category("Cat1", "", [p1])
    cat2 = Category("Cat2", "", [p2])

    assert Category.category_count == 2
    assert Category.product_count == 10 + 20  # 30 шт.


def test_product_str(product_xiaomi):
    assert str(product_xiaomi) == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт."


def test_category_str(smartphone_category):
    # Samsung 5 шт. + iPhone 8 шт. = 13 шт.
    assert str(smartphone_category) == "Смартфоны, количество продуктов: 13 шт."


def test_category_empty_str():
    category = Category("Пустая", "Нет товаров", [])
    assert str(category) == "Пустая, количество продуктов: 0 шт."


def test_product_addition(product_samsung, product_iphone):
    total = product_samsung + product_iphone
    expected = (180000.0 * 5) + (210000.0 * 8)
    assert total == expected
    assert isinstance(total, float)


def test_product_addition_with_invalid_type(product_samsung):
    with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
        product_samsung + 100


def test_zero_price_product():
    p = Product("Бесплатный", "Акционный товар", 0.0, 100)
    assert p.price == 0.0
    assert str(p) == "Бесплатный, 0.0 руб. Остаток: 100 шт."


def test_negative_quantity():
    with pytest.raises(ValueError, match="Количество товара не может быть отрицательным"):
        Product("Ошибочный", "Товар с отрицательным количеством", 100.0, -1)


def test_category_with_duplicate_products(smartphone_category, product_samsung):
    initial_count = Category.product_count
    smartphone_category.products.append(product_samsung)
    Category.product_count += product_samsung.quantity

    assert Category.product_count == initial_count + product_samsung.quantity
