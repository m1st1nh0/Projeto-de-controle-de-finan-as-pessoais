import sqlite3
from typing import Optional, List
from contextlib import contextmanager


class Database:

    def __init__(self, db_path="financas.db"):
        self.db_path = db_path
        self._criar_tabelas()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _criar_tabelas(self):
        # USUARIOS
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                remuneracao_fixa REAL NOT NULL CHECK(remuneraca_fixa >= 0),
                remuneracao_variavel REAL NOT NULL DEFAULT 0 CHECK(remuneraca_variavel >= 0),
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                        
            """
            )
            # CARTÕES
            conn.execute(
                """ 

                CREATE TABLE IF NOT EXISTS cartoes
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                limite_total REAL NOT NULL CHECK(limite_total > 0),
                limite_disponivel REAL NOT NULL CHECK(limite_disponivel >= 0),
                dia_vencimento INTEGER NOT NULL CHECK(dia_vencimento BETWEEN 1 AND 28),
                FOREING KEY (usuario_id) REFERENCES ususarios(id) ON DELETE CASCADE

                """
            )

            # FATURAS
            conn.execute(
                """ 

                CREATE TABLE IF NOT EXISTS faturas
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cartao_id INTEGER NOT NULL,
                mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AN 12),
                ano INTEGER NOT NULL CHECK(ano BETWEEN 2000 AN 2100),
                dia_vencimento INTEGER NOT NULL CHECK(dia_vencimento BETWEEN 1 AND 28),
                valor_pago REAL NOT NULL DEFAULT 0 CHECK(valor_pago >=0),
                paga BOOLEAN NOT NULL DEFAULT 0,
                FOREING KEY (cartao_id) REFERENCES cartoes(id) ON DELETE CASCADE,
                UNIQUE(cartao_id,mes,ano)

                """
            )
            # GASTOS
            conn.execute(
                """ 

                CREATE TABLE IF NOT EXISTS gastps
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cusuario_id INTEGER,
                cartao_id INTEGER,
                nome TEXT NOT NULL,
                valor REAL NOT NULL CHECK(valor > 0)
                metodo_pagamento TEXT NOT NULL CHECK(metodo_pagamento IN ('Avista','Crédito')),
                data TEXT NOT NULL,
                periodicidade TEXT NOT NULL,
                categoria TEXT NOT NULL,
                parcelas INTEGER NOT NULL DEFAULT 1 CHECK(parcelas BETWEEN 1 AND 36 ),
                FOREING KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREING KEY (fatura_id) REFERENCES faturas(id) ON DELETE SET NULL,
                
                """
            )
