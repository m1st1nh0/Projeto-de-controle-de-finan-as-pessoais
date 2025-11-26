from database import Database
from models import Usuario, CartaoDeCredito
import sqlite3


class UsuarioRepository:

    def __init__(self, database=None):
        self.db = database if database else Database()

    def salvar(self, usuario: Usuario) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO usuarios(nome, remuneracao_fixa, remuneracao_variavel)
                VALUES(?,?,?)""",
                (usuario.nome, usuario.remuneracao_fixa, usuario.remuneracao_variavel),
            )
            return cursor.lastrowid

    def buscar_por_id(self, id: int):
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            row = cursor.fetchone()

            if not row:
                return None

            usuario_id = row["id"]
            usuario = Usuario(
                nome=row["nome"],
                remuneracao_fixa=row["remuneracao_fixa"],
                remuneracao_variavel=row["remuneracao_variavel"],
            )
            usuario.id = usuario_id
            usuario.cartoes = self._carregar_cartoes(conn, usuario_id)

            return usuario

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

    def buscar_todos(self) -> list[Usuario]:
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM usuarios")
            ids = [row["id"] for row in cursor.fetchall()]
            return [self.buscar_por_id(id) for id in ids]

    def atualizar(self, usuario: Usuario):
        if not hasattr(usuario, "id"):
            raise ValueError("O usuário deve ter um ID válido para atualização.")

        with self.db.get_connection() as conn:
            conn.execute(
                """UPDATE usuarios
                SET nome = ?, remuneracao_fixa = ?, remuneracao_variavel = ?
                WHERE id = ?""",
                (
                    usuario.nome,
                    usuario.remuneracao_fixa,
                    usuario.remuneracao_variavel,
                    usuario.id,
                ),
            )

    def deletar(self, usuario_id: int):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
