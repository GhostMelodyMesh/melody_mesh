# Zmienne konfiguracyjne
COMPOSE = docker compose

# Główne komendy
.PHONY: local remote stop down clean logs ps help

# Domyślna akcja po wpisaniu `make` bez argumentów
help:
	@echo "Dostępne komendy:"
	@echo "  make local    - Uruchom aplikację z lokalną bazą danych"
	@echo "  make remote   - Uruchom aplikację ze zdalną bazą danych"
	@echo "  make stop     - Zatrzymaj wszystkie kontenery"
	@echo "  make down     - Zatrzymaj i usuń wszystkie kontenery"
	@echo "  make clean    - Zatrzymaj i usuń wszystkie kontenery oraz wolumeny"
	@echo "  make logs     - Pokaż logi wszystkich kontenerów"
	@echo "  make ps       - Pokaż status kontenerów"

# Komendy dla lokalnej bazy danych
local:
	$(COMPOSE) --profile local-db run --service-ports --rm melody-app-local bash

# Komendy dla zdalnej bazy danych
remote:
	$(COMPOSE) --profile remote-db run --service-ports --rm melody-app-remote bash

# Zatrzymanie kontenerów
stop:
	$(COMPOSE) stop

# Zatrzymanie i usunięcie kontenerów
down:
	$(COMPOSE) down --remove-orphans

# Całkowite wyczyszczenie (włącznie z wolumenami)
clean:
	$(COMPOSE) down -v --remove-orphans

# Pokazanie logów
logs:
	$(COMPOSE) logs -f

# Status kontenerów
ps:
	$(COMPOSE) ps
