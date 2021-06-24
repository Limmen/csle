%% server.pl
%% swi-prolog
%% compile: ['server.pl']
%%
%% Http+Pengine server
%%
%% Author Kim Hammar limmen@github.com <kimham@kth.se>

%%%===================================================================
%%% Facts
%%%===================================================================

:- module(pengine_server,
          [
           server/1,
           stop/1,
           sudoku/1
          ]).

:- use_module(library(clpfd)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(pengines)).
:- use_module(pengine_sandbox:library(pengines)).
:- use_module(pengine_sandbox:library(lists)).
:- use_module(library(sandbox)).
:- multifile sandbox:safe_primitive/1.
:- multifile sandbox:safe_meta_predicate/1.

%% Safe predicates accessible from remote client
sandbox:safe_primitive(lists:member(_,_)).
sandbox:sandbox_allowed_goal(sudoku(_)).
sandbox:safe_meta_predicate(shell(_)).
sandbox:safe_meta_predicate(shell(_,_)).
sandbox:safe_meta(shell(_)).
sandbox:safe_meta(shell(_,_)).
sandbox:safe_meta_primitive(shell(_)).
sandbox:safe_meta_primitive(shell(_,_)).

%%%===================================================================
%%% API
%%%===================================================================

%% Start http/pengine server on Port
%% server(+).
%% server(Port).
server(Port):-
    http_server(http_dispatch, [port(Port)]).

%% Stop http/pengine server on Port
%% stop(+).
%% stop(Port).
stop(Port):-
    http_stop_server(Port, []).

%% sudoku solver, from http://www.swi-prolog.org/pldoc/man?section=clpfd-sudoku
%% sudoku(+-).
%% sudoku(Rows).
sudoku(Rows) :-
    length(Rows, 9), maplist(same_length(Rows), Rows),
    append(Rows, Vs), Vs ins 1..9,
    maplist(all_distinct, Rows),
    transpose(Rows, Columns),
    maplist(all_distinct, Columns),
    Rows = [As,Bs,Cs,Ds,Es,Fs,Gs,Hs,Is],
    blocks(As, Bs, Cs),
    blocks(Ds, Es, Fs),
    blocks(Gs, Hs, Is).

%% helper predicate
%% blocks(+,+,+).
%% blocks( A, B, C).
blocks([], [], []).
blocks([N1,N2,N3|Ns1], [N4,N5,N6|Ns2], [N7,N8,N9|Ns3]) :-
    all_distinct([N1,N2,N3,N4,N5,N6,N7,N8,N9]),
    blocks(Ns1, Ns2, Ns3).
