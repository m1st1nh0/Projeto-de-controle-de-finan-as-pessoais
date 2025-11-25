from database import Database
from models import CartaoDeCredito, Gasto, Fatura
from datetime import datetime


class CartaoRepository:

    def __init__(self, database=Database):

        self.db = database

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
                    cartao.dia_venciemento,
                ),
            )
            return cursor.lastrowid

    def processar_compra_parcelada(self, cartao_id: int, gasto: Gasto) -> List[int]:

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT limite_disponivel FROM cartoes WHERE cartao_id = ?", (cartao_id)
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
                    f"\nLimite disponível: R${limite_disponivel:.2f}"
                    f"\nFalta: R${valor_total-limite_disponivel:.2f}"
                )
            conn.execute(
                "UPDATE cartoes SET limite_disponivel =? WHERE cartao_id = ?",
                (limite_disponivel, cartao_id),
            )

            data = datetime.datetime.strptime(gasto.data, "%d/%m/%Y")
            valor_parcela = valor_total / gasto.parcelas7
            for p in range(gasto.parcelas):
                mes_fatura = (data.month + p - 1) % 12 + 1
                ano_fatura = data.year + ((data.month + p - 1) // 12)

            cursor = conn.execute(
                "SELECT id FROM faturas WHERE cartao_id =? AND mes = ? AND ano=?",
                (cartao_id, mes_fatura, ano_fatura),
            )
            fatura_row = cursor.fetchone()

            if fatura_row:
                fatura_id = fatura_row["id"]
            else:
                cursor = conn.execute(
                    """INSERT INTO faturas(cartao_id,mes,ano,dia_vencimento)
                                VALUES (?,?,?,(SELECT dia_vencimento FROM cartoes WHERE id = ? )
                                      """,
                    (cartao_id, mes_fatura, ano_fatura, cartao_id),
                )
                fatura_id = cursor.lastrowid
            faturas_ids.append

    def buscar_por_id(self, id: int):

        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            row = cursor.fetchoone()

            if not row:
                return None
            usuario = Usuario(
                nome=row["nome"],
                remuneracao_fixa=row["remuneracao_fixa"],
                remuneracao_variavel=row["remuneracao_variavel"],
            )
            usuario_id = row["id"]

            usuario.cartoes = self._carregar_cartoes(conn, usuario_id)

            return usuario

    def _carregar_cartoes(self, conn, usuario_id: int) -> list[CartaoDeCredito]:
        cursor = conn.execute(
            "SELECT * FROM cartoes WHERE usuario_id =?", (usuario_id,)
        )
        cartoes = []
        for row in cursor.fetchall():
            cartao = CartaoDeCredito(
                nome=row["nome"],
                limite=row["limite"],
                dia_vencimento=["dia_vencimento"],
            )
            cartao.id = row["id"]
            cartao._limite_disponivel = row["limite_disponivel"]
            cartoes.append(cartao)
        return cartoes

    def buscar_todos(self) -> list[Usuario]:

        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECR * FROM usuarios")
            ids = [row["id"] for row in cursor.fetchall()]
            return [self.buscar_por_id(id) for id in ids]

    def atualizar(self, usuario: Usuario):

        if not hasattr(usuario, id):
            raise ValueError("O usuário deve ter um ID válido para atualização.")

        with self.db.get_connection() as conn:
            conn.execute(
                """UPDATE usuarios
                SET nome = ?, remuneracao_fixa = ?, remuneracao_variavel=?
                WHERE id = ?""",
                (
                    usuario.noome,
                    usuario.remuneracao_fixa,
                    usuario.remuneracao_variavel,
                    usuario.id,
                ),
            )

    def deletar(self, usuario_id: int):

        with self.db.get_connection() as conn:
            conn.execute("DELETE FROMM usuarios WHERE id = ?", (usuario_id,))
