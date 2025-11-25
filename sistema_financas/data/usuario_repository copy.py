from database import Database
from models import Usuario, CartaoDeCredito
import sqlite3


class UsuarioRepository:

    def __init__(self, database=Database):

        self.db = database

    def salvar(self, usuario: Usuario) -> int:

        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO usuarios(nome, remuneracao_fixa,remuneracao_variavel)
                VALUES(?,?,?)""",
                (usuario.nome, usuario.remuneracao_fixa, usuario.remuneracao_variavel),
            )
            return cursor.lastrowid

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
