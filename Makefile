# Inicia o ambiente Docker com banco permanente
run:
	FLASK_ENV=development DATABASE_URL=sqlite:///data/database.db docker-compose up --build

# Inicia o ambiente Docker com banco em memória
run-memory:
	FLASK_ENV=testing DATABASE_URL=sqlite:///:memory: docker-compose up --build

# Executa os testes unitários dentro do container 'web'
test:
	docker-compose run --rm web python -m unittest discover -s tests -p "*.py"

# Limpa o ambiente: remove containers, volumes e arquivos temporários
clean:
	docker-compose down --volumes --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Para os containers sem remover volumes
stop:
	docker-compose down

# Reinicia os containers para aplicar mudanças
restart:
	docker-compose restart

# Verifica os logs dos serviços
logs:
	docker-compose logs -f

# Constrói a imagem sem iniciar os containers
build:
	docker-compose build
