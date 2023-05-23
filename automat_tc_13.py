from selenium import webdriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
#Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument('--disable-dev-shm-usage')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
# Inicjalizacja przeglądarki
driver = webdriver.Chrome()
time.sleep(3)

# 1.Przejdź do strony z aplikacją "To Do List"
driver.get("https://todolist.james.am/#/")
time.sleep(3)

# Sprawdzenie czy strona zostaje otwarta
expected_title = "To Do List"
wait = WebDriverWait(driver, 10)
wait.until(EC.title_contains(expected_title))
assert expected_title in driver.title, f"Tytuł strony '{driver.title}' nie zawiera oczekiwanego adresu '{expected_title}'"

# 2.W pasku "What need's to be done" wpisz treść zadania i naciśnij enter
wait = WebDriverWait(driver, 10)
input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".new-todo")))

# Sprawdzenie czy element paska do wpisywania zadań jest widoczny na stronie
assert input_element.is_displayed(), "Element '.new-todo' nie jest obecny na stronie"
# Wpisanie zadań
zadania = ["Zrobić pranie", "Umyć okna", "Zetrzeć kurze"]
for zadanie in zadania:
    input_element.send_keys(zadanie)
    input_element.send_keys(Keys.ENTER)
    time.sleep(2)
# Oczekiwanie na pojawienie się zadań
wait = WebDriverWait(driver, 10)
lista_zadan = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".todo-list li")))
#Sprawdzenie czy wszystkie zadania (tekst zadan) są widoczne na liście
oczekiwane_zadania = [element.text for element in lista_zadan]
assert set(oczekiwane_zadania) == set(zadania), "Nie wszystkie zadania pojawiły się na liście."

# 3.Kliknij w przycisk znajdujący się po lewej stronie paska
label_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Mark all as complete')]")))
label_element.click()
wait = WebDriverWait(driver,15)
time.sleep(5)
# Sprawdzenie czy element do oznaczania wszystkich zadan jako zakonczone jest widoczny na stronie
assert driver.find_element(By.XPATH, "//label[contains(., 'Mark all as complete')]").is_displayed()
# Sprawdzenie czy zadania zostały oznaczone jako completed
lista_zadan = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'ng-scope completed')]")))

assert len(lista_zadan) == len(zadania), "Nie wszystkie zadania zostały oznaczone jako completed"
# Sprawdź czy checkboxy obok zadań są zaznaczone
lista_zadan = driver.find_elements(By.CSS_SELECTOR, ".todo-list li")
for element in lista_zadan:
    nazwa_zadania = element.find_element(By.XPATH, "//input[@type='checkbox']").text
    is_completed = "completed" in element.get_attribute("class")

    assert is_completed, "Checkboxy nie są zaznaczone"

#Sprawdź czy completed jest obecny na stronie
assert driver.find_element(By.XPATH,"//a[contains(text(),'Completed')]").is_displayed()

# 4. Przejdź do completed
completed_element = driver.find_element(By.XPATH, "//a[contains(text(),'Completed')]")
completed_element.click()
#Sprawdź czy completed jest zaznaczony
completed_element = driver.find_element(By.XPATH, "//a[contains(text(),'Completed')]")
is_selected = "selected" in completed_element.get_attribute("class")
assert is_selected, "Przycisk 'Completed' nie jest zaznaczony"
time.sleep(3)
# Sprawdź czy zadania są widoczne na liście completed
completed_tasks = driver.find_elements(By.CSS_SELECTOR, ".todo-list li.completed")
assert len(completed_tasks) > 0, "Na liście brak zadań oznaczonych jako 'completed'."
time.sleep(3)

#Sprawdź czy ALl jest widoczne na stronie
assert driver.find_element(By.XPATH,"//a[contains(text(),'All')]").is_displayed()

#5. Przejdź do sekcji All
all_element = driver.find_element(By.XPATH,"//a[contains(text(),'All')]")
all_element.click()
#Sprawdź czy all jest wybrany
all_element = driver.find_element(By.XPATH,"//a[contains(text(),'All')]")
is_selected = "selected" in all_element.get_attribute("class")
assert is_selected, "Przycisk All nie jest zaznaczony"
time.sleep(3)
#Sprawdź czy zadania w stanie completed są widoczne w All
completed_tasks = driver.find_elements(By.CSS_SELECTOR, ".todo-list li.completed")
assert len(completed_tasks) > 0, "Na liście brak zadań oznaczonych jako 'completed'."
time.sleep(3)
# 7. Kliknij podwojnie w element "Mark all as complete"
label_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Mark all as complete')]")))
label_element.click()
time.sleep(3)
label_element.click()
time.sleep(3)

# Sprawdzenie czy zadania zostały odznaczone jako completed
lista_zadan = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'ng-scope')]")))
assert len(lista_zadan) == len(zadania), "Nie wszystkie elementy zostały odznaczone jako completed"

time.sleep(3)
# Sprawdź czy checkboxy obok zadań są odznaczone
lista_zadan = driver.find_elements(By.CSS_SELECTOR, ".todo-list li")
for element in lista_zadan:
    nazwa_zadania = element.find_element(By.XPATH, "//input[@type='checkbox']").text
    is_completed = "completed" not in element.get_attribute("class")
    assert is_completed, "Checkboxy nie są zaznaczone"
# Kliknij w element "Completed"
completed_element = driver.find_element(By.XPATH, "//a[contains(text(),'Completed')]")
completed_element.click()
completed_element = driver.find_element(By.XPATH, "//a[contains(text(),'Completed')]")
is_selected = "selected" in completed_element.get_attribute("class")
assert is_selected, "Przycisk 'Completed' nie jest wybrany"
# Sprawdź czy nie ma zadań na tej liście
completed_tasks = driver.find_elements(By.CSS_SELECTOR, ".todo-list li.completed")
assert len(completed_tasks) == 0, "UPS - na liście są zadania oznaczone jako 'completed'"

time.sleep(3)
try:
    assert len(completed_tasks) == 0, "UPS - na liście są zadania oznaczone jako 'completed'"

    # Jeżeli ostatnia asercja jest poprawna oznacza to, że test został wykonany poprawnie i wszystkie założenia zostały osiągnięte
    print("Test wykonany poprawnie!")
except AssertionError as e:
    # Jeżeli wystąpił błąd asercji
    print(f"Błąd asercji: {e}")
except Exception as e:
    # Jeżeli wystąpił inny błąd
    print(f"Inny błąd: {e}")


# Zamknięcie przeglądarki
driver.quit()
