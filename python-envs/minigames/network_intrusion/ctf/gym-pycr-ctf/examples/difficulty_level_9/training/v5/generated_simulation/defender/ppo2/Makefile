.PHONY: clean tensorboard plots

run: run.py run.sh
	./run.sh

run_server: run.py run_server.sh
	./run_server.sh

run_server_no_config: run.py run_server_no_config.sh
	./run_server_no_config.sh

tensorboard:
	tensorboard --logdir=./tensorboard

plots:
	./make_plots.sh

all: run

clean:
	rm -rf results data logs plots hyperparameters gifs videos tensorboard nohup.out