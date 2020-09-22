run: synos/__init__.py
	@echo Launching bot...
	@python main.py

clean: synos/__pycache__
	rm -rf synos/__pycache__