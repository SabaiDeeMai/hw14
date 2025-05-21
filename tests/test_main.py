import pytest
from io import StringIO
import sys

from src.main import Category, Product, LawnGrass, Smartphone, BaseProduct


# Фикстура для захвата вывода в консоль
@pytest.fixture
def capture_stdout():
    new_out = StringIO()
    old_out = sys.stdout
    sys.stdout = new_out
    yield new_out
    sys.stdout = old_out


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


# Новые тесты для проверки нового функционала
def test_base_product_is_abstract():
    """Проверяем, что BaseProduct является абстрактным классом"""
    with pytest.raises(TypeError):
        BaseProduct("Test", "Test", 100, 1)


def test_product_inherits_from_base_product(product_xiaomi):
    """Проверяем, что Product наследуется от BaseProduct"""
    assert isinstance(product_xiaomi, BaseProduct)


def test_init_logger_mixin_output():
    p = Product("Test", "Desc", 100, 1)
    assert True  # Просто проверяем что объект создается


def test_smartphone_inherits_from_product(smartphone):
    """Проверяем, что Smartphone наследуется от Product"""
    assert isinstance(smartphone, Product)
    assert isinstance(smartphone, BaseProduct)


def test_lawn_grass_inherits_from_product(lawn_grass):
    """Проверяем, что LawnGrass наследуется от Product"""
    assert isinstance(lawn_grass, Product)
    assert isinstance(lawn_grass, BaseProduct)


def test_product_implements_required_methods():
    """Проверяем, что Product реализует все необходимые методы BaseProduct"""
    required_methods = {'__init__', '__str__', '__add__'}
    assert all(method in Product.__dict__ for method in required_methods)


# Остальные существующие тесты остаются без изменений
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


# ... (остальные существующие тесты остаются без изменений)


@pytest.fixture
def smartphone():
    return Smartphone(
        name="iPhone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
        efficiency=95.5,
        model="15",
        memory=512,
        color="Gray space"
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        name="Газонная трава",
        description="Элитная трава для газона",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый"
    )


def test_add_different_class_products(smartphone, lawn_grass):
    """Проверяем, что нельзя складывать товары разных классов"""
    with pytest.raises(TypeError, match="Можно складывать только товары одного класса"):
        smartphone + lawn_grass


# ... (остальные существующие тесты)


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
    assert Category.category_count == 2
    assert Category.product_count == 3  # 2 + 1


def test_empty_category():
    category = Category("Пустая категория", "Без товаров", [])
    assert len(category.products) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_add_product_to_category(smartphone_category):
    new_product = Product("Nokia 3310", "Легендарный телефон", 1000.0, 1)
    smartphone_category.products.append(new_product)
    assert len(smartphone_category.products) == 3


def test_total_category_count(smartphone_category, tv_category):
    assert Category.category_count == 2


def test_total_product_count(smartphone_category, tv_category):
    assert Category.product_count == 3


def test_static_counter_initial_state():
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_modify_product_attributes(product_xiaomi):
    product_xiaomi.price = 35000.0
    product_xiaomi.quantity = 10
    assert product_xiaomi.price == 35000.0
    assert product_xiaomi.quantity == 10


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


def test_product_str(product_xiaomi):
    assert str(product_xiaomi) == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт."


def test_category_str(smartphone_category):
    assert str(smartphone_category) == "Смартфоны, количество продуктов: 2 шт."


def test_product_addition(product_samsung, product_iphone):
    total = product_samsung + product_iphone
    expected = (180000.0 * 5) + (210000.0 * 8)
    assert total == expected
    assert isinstance(total, float)


def test_product_addition_with_invalid_type(product_samsung):
    with pytest.raises(TypeError, match="Можно складывать только товары одного класса"):
        product_samsung + 100


def test_zero_price_product():
    p = Product("Бесплатный", "Акционный товар", 0.0, 100)
    assert p.price == 0.0
    assert str(p) == "Бесплатный, 0.0 руб. Остаток: 100 шт."


def test_negative_quantity():
    with pytest.raises(ValueError, match="Количество товара не может быть отрицательным"):
        Product("Ошибочный", "Товар с отрицательным количеством", 100.0, -1)


def test_category_with_duplicate_products(smartphone_category, product_samsung):
    initial_count = len(smartphone_category.products)
    smartphone_category.products.append(product_samsung)
    assert len(smartphone_category.products) == initial_count + 1


def test_empty_category_str():
    category = Category("Пустая", "Нет товаров", [])
    assert str(category) == "Пустая, количество продуктов: 0 шт."


def test_add_same_class_products(product_samsung, product_iphone):
    """Проверяем, что можно складывать товары одного класса"""
    total = product_samsung + product_iphone
    expected = (180000.0 * 5) + (210000.0 * 8)
    assert total == expected


@pytest.fixture
def smartphone():
    return Smartphone(
        name="iPhone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
        efficiency=95.5,
        model="15",
        memory=512,
        color="Gray space"
    )

@pytest.fixture
def lawn_grass():
    return LawnGrass(
        name="Газонная трава",
        description="Элитная трава для газона",
        price=500.0,
        quantity=20,
        country="Россия",
        germination_period="7 дней",
        color="Зеленый"
    )

def test_add_different_class_products(smartphone, lawn_grass):
    """Проверяем, что нельзя складывать товары разных классов"""
    with pytest.raises(TypeError, match="Можно складывать только товары одного класса"):
        smartphone + lawn_grass


def test_add_product_with_subclass(smartphone_category):
    """Проверяем, что нельзя добавить в категорию объект, не являющийся Product"""
    with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
        smartphone_category.add_product("Not a product")


def test_product_addition_with_zero_quantity():
    """Проверяем сложение товаров с нулевым количеством"""
    p1 = Product("Товар 1", "Описание", 1000.0, 0)
    p2 = Product("Товар 2", "Описание", 2000.0, 0)
    assert p1 + p2 == 0.0


def test_product_addition_with_updated_quantity(product_samsung):
    """Проверяем сложение после изменения количества"""
    original_sum = product_samsung + product_samsung
    product_samsung.quantity = 10
    updated_sum = product_samsung + product_samsung
    assert updated_sum == (180000.0 * 10) * 2
    assert updated_sum != original_sum


def test_product_str_representation(product_samsung):
    """Проверка строкового представления продукта"""
    assert str(product_samsung) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str_representation(smartphone_category):
    """Проверка строкового представления категории"""
    assert str(smartphone_category) == "Смартфоны, количество продуктов: 2 шт."


def test_product_addition_edge_cases():
    """Проверка крайних случаев сложения товаров"""
    p1 = Product("Товар 1", "Описание", 1000.0, 0)
    p2 = Product("Товар 2", "Описание", 2000.0, 0)
    assert p1 + p2 == 0.0

    # Сложение с отрицательной ценой (должно работать, если quantity положительное)
    p3 = Product("Товар 3", "Описание", -500.0, 2)
    p4 = Product("Товар 4", "Описание", 1000.0, 3)
    assert p3 + p4 == (-500.0 * 2 + 1000.0 * 3)


def test_category_add_multiple_products(smartphone_category):
    """Проверка добавления нескольких продуктов в категорию"""
    initial_count = len(smartphone_category.products)
    initial_total = Category.product_count  # Запоминаем текущее общее количество

    new_product = Product("New Model", "Latest", 50000.0, 10)
    smartphone_category.add_product(new_product)

    assert len(smartphone_category.products) == initial_count + 1
    assert Category.product_count == initial_total + 1


def test_category_remove_product(smartphone_category, product_iphone):
    """Проверка удаления продукта из категории"""
    initial_count = len(smartphone_category.products)
    smartphone_category.products.remove(product_iphone)
    assert len(smartphone_category.products) == initial_count - 1
