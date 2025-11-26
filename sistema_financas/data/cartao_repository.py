from database import Database
from models import CartaoDeCredito, Gasto, Fatura, Usuario
from datetime import datetime
from typing import List


class CartaoRepository:

    def __init__(self, database=None):
        self.db = database if database else Database()

    def salvar(self, cartao: CartaoDeCredito, usuario_id: int) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO cartoes(usuario_id, nome, limite_total, limite_disponivel, dia_vencimento)
                VALUES(?,?,?,?,?)""",
                (
                    usuario_id,
                    cartao.nome,
                    cartao.limite_total,
                    cartao.limite_disponivel,
                    cartao.dia_vencimento,
                ),
            )
            return cursor.lastrowid

    def processar_compra_parcelada(self, cartao_id: int, gasto: Gasto) -> List[int]:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT limite_disponivel FROM cartoes WHERE cartao_id = ?",
                (cartao_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError("Cartão não encontrado.")
            limite_disponivel = row["limite_disponivel"]
            valor_total = gasto.valor

            if limite_disponivel < valor_total:
                raise ValueError(
                    f"Limite Insuficiente!"
                    f"\nLimite disponível: R${limite_disponivel:.2f}"
                    f"\nValor da compra: R${valor_total:.2f}"
                    f"\nFalta: R${valor_total-limite_disponivel:.2f}"
                )
            conn.execute(
                "UPDATE cartoes SET limite_disponivel = ? WHERE cartao_id = ?",
                (limite_disponivel - valor_total, cartao_id),
            )

            data = datetime.strptime(gasto.data, "%d/%m/%Y")
            valor_parcela = valor_total / gasto.parcelas
            faturas_ids = []
            for p in range(gasto.parcelas):
                mes_fatura = (data.month + p - 1) % 12 + 1
                ano_fatura = data.year + ((data.month + p - 1) // 12)

                cursor = conn.execute(
                    "SELECT id FROM faturas WHERE cartao_id = ? AND mes = ? AND ano = ?",
                    (cartao_id, mes_fatura, ano_fatura),
                )
                fatura_row = cursor.fetchone()

                if fatura_row:
                    fatura_id = fatura_row["id"]
                else:
                    cursor = conn.execute(
                        """INSERT INTO faturas(cartao_id, mes, ano, dia_vencimento)
                        VALUES (?, ?, ?, (SELECT dia_vencimento FROM cartoes WHERE id = ?))""",
                        (cartao_id, mes_fatura, ano_fatura, cartao_id),
                    )
                    fatura_id = cursor.lastrowid
                faturas_ids.append(fatura_id)

                nome_parcela = f"{gasto.nome} - Parcela {p+1}/{gasto.parcelas}"

                conn.execute(
                    """INSERT INTO gastos
                    (fatura_id, nome, valor, metodo_pagamento, data, periodicidade, categoria, parcelas)
                    VALUES(?,?,?,?,?,?,?,1)""",
                    (
                        fatura_id,
                        nome_parcela,
                        valor_parcela,
                        gasto.metodo_pagamento,
                        gasto.data,
                        gasto.periodicidade,
                        gasto.categoria,
                    ),
                )
            return faturas_ids

    def buscar_por_id(self, id: int):
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM cartoes WHERE id = ?", (id,))
            row = cursor.fetchone()

            if not row:
                return None
            cartao = CartaoDeCredito(
                nome=row["nome"],
                limite_total=row["limite_total"],
                limite_disponivel=row["limite_disponivel"],
            )
            cartao.id = row["id"]
            cartao.dia_vencimento = row["dia_vencimento"]

            return cartao

    def _carregar_cartoes(self, conn, usuario_id: int) -> list[CartaoDeCredito]:
        cursor = conn.execute(
            "SELECT * FROM cartoes WHERE usuario_id = ?", (usuario_id,)
        )
        cartoes = []
        for row in cursor.fetchall():
            cartao = CartaoDeCredito(
                nome=row["nome"],
                limite_total=row["limite_total"],
                dia_vencimento=row["dia_vencimento"],
            )
            cartao.id = row["id"]
            cartao.limite_disponivel = row["limite_disponivel"]
            cartoes.append(cartao)
        return cartoes

    def buscar_todos(self) -> list[CartaoDeCredito]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM cartoes")
            ids = [row["id"] for row in cursor.fetchall()]
            return [self.buscar_por_id(id) for id in ids]

    def atualizar(self, cartao: CartaoDeCredito):
        if not hasattr(cartao, "id"):
            raise ValueError("O cartão deve ter um ID válido para atualização.")

        with self.db.get_connection() as conn:
            conn.execute(
                """UPDATE cartoes
                SET nome = ?, limite_total = ?, limite_disponivel = ?, dia_vencimento = ?
                WHERE id = ?""",
                (
                    cartao.nome,
                    cartao.limite_total,
                    cartao.limite_disponivel,
                    cartao.dia_vencimento,
                    cartao.id,
                ),
            )

    def deletar(self, cartao_id: int):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM cartoes WHERE id = ?", (cartao_id,))
