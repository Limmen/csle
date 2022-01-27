%% daemon.pl
%% swi-prolog
%% compile: ['daemon.pl']
%%
%% Starts the http server as a unix daemon.
%% See http://www.swi-prolog.org/pldoc/man?section=http-running-server for documentation
%% Example commands:
%% to start: prolog daemon.pl --http=4000 --pidfile=pid/http.pid
%% to stop: cat pid/http.pid | xargs kill -9
%%
%% Author Kim Hammar limmen@github.com <kimham@kth.se>

%%%===================================================================
%%% Facts
%%%===================================================================

:- use_module(library(http/http_unix_daemon)).
:- initialization http_daemon.
:- [server].