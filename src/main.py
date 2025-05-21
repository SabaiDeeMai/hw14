from abc import ABC, abstractmethod
from typing import List


class InitLoggerMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        positional_args = ", ".join(repr(arg) for arg in args)
        keyword_args = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [positional_args, keyword_args]))
        print(f"Создан объект класса {class_name} с параметрами: {all_args}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """Абстрактный базовый класс для товаров"""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class Product(BaseProduct, InitLoggerMixin):
    def __init__(self, name, description, price, quantity):
        super().__init__(name=name, description=description, price=price, quantity=quantity)

        if quantity < 0:
            raise ValueError("Количество товара не может быть отрицательным")
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Можно складывать только товары одного класса")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """Класс описывает смартфон"""

    def __init__(self, name, description, price, quantity,
                 efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс описывает газонную траву"""

    def __init__(self, name, description, price, quantity,
                 country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс описывает категорию товаров"""

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = list(products)

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.products)} шт."

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")

        self.products.append(product)
        Category.product_count += 1


if __name__ == '__main__':
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1)
    print(smartphone2)
    print(smartphone3)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1)
    print(grass2)

    smartphone_sum = smartphone1 + smartphone2
    print(f"Суммарная стоимость смартфонов: {smartphone_sum}")

    grass_sum = grass1 + grass2
    print(f"Суммарная стоимость газонной травы: {grass_sum}")

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError as e:
        print(f"Ошибка: {e}")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)
    print(f"Продукты в категории 'Смартфоны': {category_smartphones.products}")
    print(f"Общее количество продуктов: {Category.product_count}")

    try:
        category_smartphones.add_product("Not a product")
    except TypeError as e:
        print(f"Ошибка при добавлении не продукта: {e}")
