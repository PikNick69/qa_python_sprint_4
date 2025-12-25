from main import BooksCollector
import pytest


class TestBooksCollector:
    def test_add_new_book_valid_name(self, collector):
        collector.add_new_book("Властелин колец")
        assert "Властелин колец" in collector.books_genre
        assert collector.books_genre["Властелин колец"] == ""

    @pytest.mark.parametrize('book_name, should_be_added', [
         ('', False),
         ('Книга', True),
         ('b' * 40, True),
         ('b' * 41, False),
    ])
    def test_add_new_book_boundary_values(self, collector, book_name, should_be_added):
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == should_be_added

    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Марсианин")
        collector.set_book_genre("Марсианин", "Фантастика")
        assert collector.get_book_genre("Марсианин") == "Фантастика"
        
    def test_set_book_genre_nonexistent_book(self, collector):
        collector.add_new_book("Тестовая")
        initial_state = collector.get_books_genre()
        collector.set_book_genre("Несуществующая", "Комедии")
        assert collector.get_books_genre() == initial_state
    
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Фантастика")
        books = collector.get_books_with_specific_genre("Фантастика")
        assert len(books) == 2
        assert "Книга1" in books and "Книга2" in books

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Мультик")
        collector.add_new_book("Ужастик")
        collector.set_book_genre("Мультик", "Мультфильмы")
        collector.set_book_genre("Ужастик", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Мультик" in children_books
        assert "Ужастик" not in children_books

    def test_add_book_in_favorites(self, collector):
        collector.add_new_book("Избранная")
        collector.add_book_in_favorites("Избранная")
        assert "Избранная" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_no_duplicates(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        assert collector.get_list_of_favorites_books().count("Книга") == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.get_list_of_favorites_books()

    def test_get_books_genre_returns_current_dictionary(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        assert collector.get_books_genre() == {"Книга1": "Фантастика", "Книга2": ""}

@pytest.fixture
def collector():
    return BooksCollector()