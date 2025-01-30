# System Zarządzania Zasobami Szpitala
## Opis projektu
System Zarządzania Zasobami Szpitala to kompleksowa aplikacja webowa stworzona w Django, której celem jest efektywne zarządzanie zasobami szpitala. System umożliwia administrację pacjentami, personelem medycznym, salami szpitalnymi oraz rezerwacjami, co pozwala na optymalizację pracy szpitala i zwiększenie efektywności operacyjnej.
## Kluczowe funkcjonalności
Zarządzanie pacjentami</br>
Przechowywanie danych osobowych i medycznych</br>
Historia pobytów i leczenia</br>
Zarządzanie personelem</br>
Rejestracja i zarządzanie lekarzami, pielęgniarkami i innymi pracownikami</br>
Zarządzanie salami szpitalnymi</br>
Przegląd dostępnych sal</br>
Dodawanie, edycja i usuwanie sal</br>
Monitorowanie zajętości sal</br>
Rezerwacje i harmonogram</br>
Tworzenie rezerwacji dla pacjentów (np. na badania, operacje, wizyty)</br>
Zarządzanie dostępnością sal i lekarzy</br>
Powiadomienia o nadchodzących terminach</br>
System autoryzacji i uprawnień</br>
Uwierzytelnianie użytkowników </br>
Uprawnienia oparte na rolach</br>
## Cel projektu
System Zarządzania Zasobami Szpitala ma na celu zwiększenie efektywności zarządzania placówką medyczną poprzez cyfryzację procesów organizacyjnych. System ułatwia koordynację pracy personelu, usprawnia przepływ pacjentów i pozwala na optymalne wykorzystanie dostępnych zasobów. Dzięki intuicyjnemu interfejsowi i integracji z bazą danych użytkownicy mogą szybko uzyskać potrzebne informacje oraz efektywnie zarządzać szpitalem.
## Struktura plików
.</br>
├── admin.py</br>
├── apps.py</br>
├── context_processors.py</br>
├── decorators.py</br>
├── __init__.py</br>
├── migrations</br>
│   ├── 0001_initial.py</br>
│   ├── 0002_staff_user.py</br>
│   ├── 0003_reservation.py</br>
│   ├── 0004_room_capacity.py</br>
│   ├── 0005_reservation_description.py</br>
│   ├── __init__.py</br>
│   └── __pycache__</br>
│       ├── 0001_initial.cpython-310.pyc</br>
│       ├── 0002_staff_user.cpython-310.pyc</br>
│       ├── 0003_reservation.cpython-310.pyc</br>
│       ├── 0004_room_capacity.cpython-310.pyc</br>
│       ├── 0005_reservation_description.cpython-310.pyc</br>
│       └── __init__.cpython-310.pyc</br>
├── models.py</br>
├── __pycache__</br>
│   ├── apps.cpython-310.pyc</br>
│   ├── context_processors.cpython-310.pyc</br>
│   ├── decorators.cpython-310.pyc</br>
│   ├── __init__.cpython-310.pyc</br>
│   ├── models.cpython-310.pyc</br>
│   ├── urls.cpython-310.pyc</br>
│   ├── utils.cpython-310.pyc</br>
│   └── views.cpython-310.pyc</br>
├── tests.py</br>
├── urls.py</br>
├── utils.py</br>
└── views.py</br>


## Funkcjonalnosci/Endpointy
<details>
<summary>Strona główna</summary>
<ul>
<li>Endpoint: `/` oraz `/home/`</li>
<li>Opis: Wyświetla stronę główną aplikacji.</li>
</ul>
</details>
<details>
<summary>Lista personelu</summary>
<ul>
<li>Endpoint: `/staff/`</li>
<li>Opis: Wyświetla listę wszystkich członków personelu.</li>
</ul>
</details>
<details>
<summary>Lista pacjentów</summary>
<ul>
<li>Endpoint: `/patients/`</li>
<li>Opis: Wyświetla listę wszystkich pacjentów.</li>
</ul>
</details>
<details>
<summary>Lista pokoi</summary>
<ul>
<li>Endpoint: `/rooms/`</li>
<li>Opis: Wyświetla listę dostępnych pokoi.</li>
</ul>
</details>
<details>
<summary>Dodawanie pokoju</summary>
<ul>
<li>Endpoint: `/add_room/`</li>
<li>Opis: Formularz do dodania nowego pokoju.</li>
</ul>
</details>
<details>
<summary>Dodawanie pacjenta</summary>
<ul>
<li>Endpoint: `/add_patient/`</li>
<li>Opis: Formularz do dodania nowego pacjenta.</li>
</ul>
</details>
<details>
<summary>Logowanie</summary>
<ul>
<li>Endpoint: `/login/`</li>
<li>Opis: Strona logowania użytkownika.</li>
</ul>
</details>
<details>
<summary>Wylogowanie</summary>
<ul>
<li>Endpoint: `/logout/`</li>
<li>Opis: Wylogowuje użytkownika i przekierowuje na stronę logowania.</li>
</ul>
</details>
<details>
<summary>Dodawanie personelu</summary>
<ul>
<li>Endpoint: `/add_staff/`</li>
<li>Opis: Formularz do dodania nowego pracownika personelu.</li>
</ul>
</details>
<details>
<summary>Edytowanie pacjenta</summary>
<ul>
<li>Endpoint: `/edit_patient/`</li>
<li>Opis: Edytuje dane pacjenta.</li>
</ul>
</details>
<details>
<summary>Usuwanie pacjenta</summary>
<ul>
<li>Endpoint: `/delete_patient/&lt;int:patient_id&gt;/`</li>
<li>Opis: Usuwa pacjenta na podstawie ID.</li>
</ul>
</details>
<details>
<summary>Pobieranie danych pacjenta</summary>
<ul>
<li>Endpoint: `/get_patient/&lt;int:patient_id&gt;/`</li>
<li>Opis: Pobiera dane pacjenta w formacie JSON.</li>
</ul>
</details>
<details>
<summary>Pobieranie danych pokoju</summary>
<ul>
<li>Endpoint: `/get_room/&lt;int:room_id&gt;/`</li>
<li>Opis: Pobiera dane pokoju w formacie JSON.</li>
</ul>
</details>
<details>
<summary>Pobieranie danych personelu</summary>
<ul>
<li>Endpoint: `/get_staff/&lt;int:staff_id&gt;/`</li>
<li>Opis: Pobiera dane pracownika personelu w formacie JSON.</li>
</ul>
</details>
<details>
<summary>Usuwanie pokoju</summary>
<ul>
<li>Endpoint: `/delete_room/&lt;int:room_id&gt;/`</li>
<li>Opis: Usuwa pokój na podstawie ID.</li>
</ul>
</details>
<details>
<summary>Usuwanie personelu</summary>
<ul>
<li>Endpoint: `/delete_staff/&lt;int:staff_id&gt;/`</li>
<li>Opis: Usuwa pracownika personelu na podstawie ID.</li>
</ul>
</details>
<details>
<summary>Edytowanie personelu</summary>
<ul>
<li>Endpoint: `/edit_staff/&lt;int:staff_id&gt;/`</li>
<li>Opis: Edytuje dane pracownika personelu.</li>
</ul>
</details>
<details>
<summary>Edytowanie pokoju</summary>
<ul>
<li>Endpoint: `/edit_room/&lt;int:room_id&gt;/`</li>
<li>Opis: Edytuje dane pokoju.</li>
</ul>
</details>
<details>
<summary>Lista rezerwacji</summary>
<ul>
<li>Endpoint: `/reservations/`</li>
<li>Opis: Wyświetla listę wszystkich rezerwacji.</li>
</ul>
</details>
<details>
<summary>Dodawanie rezerwacji</summary>
<ul>
<li>Endpoint: `/add_reservation/`</li>
<li>Opis: Formularz do dodania nowej rezerwacji.</li>
</ul>
</details>
<details>
<summary>Usuwanie rezerwacji</summary>
<ul>
<li>Endpoint: `/delete_reservation/&lt;int:reservation_id&gt;/`</li>
<li>Opis: Usuwa rezerwację na podstawie ID.</li>
</ul>
</details>
<details>
<summary>Sprawdzenie dostępności pokoju</summary>
<ul>
<li>Endpoint: `/room_availability/&lt;int:room_id&gt;/`</li>
<li>Opis: Zwraca dostępność pokoju w danym miesiącu.</li>
</ul>
</details>
<details>
<summary>Szczegóły rezerwacji</summary>
<ul>
<li>Endpoint: `/reservation_details/&lt;int:reservation_id&gt;/`</li>
<li>Opis: Pobiera szczegóły rezerwacji.</li>
</ul>
</details>
<details>
<summary>Rezerwacje pacjenta</summary>
<ul>
<li>Endpoint: `/patient/&lt;int:patient_id&gt;/reservations/`</li>
<li>Opis: Wyświetla rezerwacje dla konkretnego pacjenta.</li>
</ul>
</details>
<details>
<summary>Pobieranie danych rezerwacji</summary>
<ul>
<li>Endpoint: `/get_reservation/&lt;int:reservation_id&gt;/`</li>
<li>Opis: Pobiera dane rezerwacji w formacie JSON.</li>
</ul>
</details>
<details>
<summary>Edytowanie rezerwacji</summary>
<ul>
<li>Endpoint: `/edit_reservation/`</li>
<li>Opis: Edytuje istniejącą rezerwację.</li>
</ul>
</details>
<details>
<summary>Rezerwacje pokoju</summary>
<ul>
<li>Endpoint: `/room_reservations/&lt;int:room_id&gt;/`</li>
<li>Opis: Wyświetla listę rezerwacji dla danego pokoju.</li>
</ul>
</details>

## Struktura Bazy danych
```
+------------------+        +--------------------+      +-------------------+
|      Room        |        |    Patient         |      |      Staff        |
+------------------+        +--------------------+      +-------------------+
| id (PK)          |        | id (PK)            |      | id (PK)           |
| name             |        | first_name         |      | user (FK)         |
| type             |        | last_name          |      | first_name        |
| description      |        | birth_date         |      | last_name         |
| room_number      |        | registration_date  |      | position          |
| capacity         |        | registered_by (FK) |      | role              |
+------------------+        +--------------------+      +-------------------+
       |                           |                          |
       +---------------------------+--------------------------+
                                   |
                           +-------------------+
                           |    Reservation    |
                           +-------------------+
                           | id (PK)           |
                           | patient (FK)      |
                           | room (FK)         |
                           | start_date        |
                           | end_date          |
                           | description       |
                           +-------------------+
```
