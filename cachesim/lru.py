class _Node:
    def __init__(self,page:int):
        """узел двусвязного списка для хранения страницы в LRU"""
        self.page = page 
        self.prev = None
        self.next = None
        self.hits = 0
        self.misses = 0
class LRU:
    def __init__(self,capacity:int):
        self.capacity = capacity
        self.head = None # самый свежий узел
        self.tail = None # самый старый узел
        self._nodes = {} # хэш-таблица для быстрого доступа к узлам по номеру страницы
        self.hits = 0
        self.misses = 0
    def add_to_front(self, node:_Node) -> None:
        node.prev = None
        node.next = self.head
        
        if self.head:
            # 1 случай в списке были узлф
            self.head.prev = node
        else:
            # 2 случай список был пустой
            self.tail = node
        self.head = node
    def remove(self, node: _Node) -> None:
        """Удаляет узел из двусвязного списка и связывает его бывших соседей напрямую."""
        # 1.разбираемся с левым соседом или головой
        if node is self.head:
            self.head = node.next
        else:
            node.prev.next = node.next

        # 2.разбираемся с правым соседом или хвостом
        if node is self.tail:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        # 3. Изолируем узел 
        node.prev = None
        node.next = None
    def move_to_front(self, node: _Node) -> None:
        """Перемещает существующий узел в начало списка при попадании (hit)."""
        self.remove(node)
        self.add_to_front(node)

    def pop_last(self) -> _Node | None:
        """Удаляет и возвращает самый старый узел (tail) для вытеснения.
        
        Если список пуст, возвращает None.
        """
        if self.tail is None:
            return None

        node = self.tail
        self.remove(node)
        return node
    def access(self, page: int) -> bool:
        """Обрабатывает обращение к странице.
        
        Возвращает True при попадании (hit) и False при промахе (miss).
        """
        # 1. Попадание (Hit)
        if page in self._nodes:
            node = self._nodes[page]
            self.move_to_front(node)
            self.hits += 1
            return True

        self.misses += 1

        # Если кэш полон — вытесняем кандидата из хвоста
        if len(self._nodes) == self.capacity:
            evicted = self.pop_last()
            if evicted is not None:
                del self._nodes[evicted.page]

        # Создаём новый узел, ставим в голову и сохраняем в словарь
        new_node = _Node(page)
        self.add_to_front(new_node)
        self._nodes[page] = new_node

        return False
    def to_list(self) -> list[int]:
        """Возвращает список страниц от головы (свежие) к хвосту (старые)."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.page)
            current = current.next
        return result
if __name__ == "__main__":
    cache = LRU(3)
    trace = [1, 2, 3, 1, 4, 2, 5, 1]

    for p in trace:
        is_hit = cache.access(p)
        status = "HIT " if is_hit else "MISS"
        print(f"Запрос {p} -> {status} | Кэш (head->tail): {cache.to_list()}")

    print("\nИтог")
    print(f"Hits: {cache.hits}, Misses: {cache.misses}")
    print(f"Финальное состояние кэша: {cache.to_list()}")

    assert cache.hits == 1, f"Ожидался 1 hit, получено {cache.hits}"
    assert cache.misses == 7, f"Ожидалось 7 misses, получено {cache.misses}"
    assert cache.to_list() == [1, 5, 2], f"Ожидалось [1, 5, 2], получено {cache.to_list()}"
    print("Все проверки пройдены успешно!")
