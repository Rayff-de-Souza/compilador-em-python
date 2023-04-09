# COMPILADOR EM PYTHON

> Autor: Ícaro Rayff

> Data de criação: 09/04/2023

## 1. Objetivo
O objetivo deste programa é simular algumas funcionalidades básicas de um processador, sendo a ULA (unidade lógica aritmética) e a unidade de controle.

## 2. Organização dos arquivos
Com isso em mente, os arquivos estão distribuídos da seguinte forma:

### 2.1 Arquivos_memoria
Nesta pasta temos todos os arquivos binários que o programa poderá executar, dos menos complexos até os mais complexos.

### 2.2 main.py
Aqui temos o fluxo principal do nosso código. É neste arquivo onde teremos as funções que interpretarão a ULA e a unidade de controle.

### 2.3 MemoriaCache.py
Este aquivo ficará responsável por guardar nosso programa em memória e retornar o nosso ponteiro, para assim podermos procurar a próxima instrução.