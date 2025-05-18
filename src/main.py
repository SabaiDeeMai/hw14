from typing import List


from typing import List


class Product:
    """Класс описывает товар"""

    def __init__(self, name, description, price, quantity):
        if quantity < 0:
            raise ValueError("Количество товара не может быть отрицательным")
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.quantity: int = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Класс описывает категорию товаров"""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products):
        self.name: str = name
        self.description: str = description
        self.products: List[Product] = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {len(self.products)} шт."


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
