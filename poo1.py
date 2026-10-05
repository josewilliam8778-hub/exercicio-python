class Endereco:
    """Existe independentemente do aluno (agregação)."""

    def __init__(self, rua, numero, cidade):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade

    def formatar(self):
        return f"{self.rua}, {self.numero} - {self.cidade}"


class Aluno:
    """Agrega um Endereco: o endereço é criado junto com o cadastro,
    mas sobrevive à remoção do aluno."""

    def __init__(self, nome, matricula, rua, numero, cidade):
        self.nome = nome
        self.matricula = matricula
        self.endereco = Endereco(rua, numero, cidade)

    def mudar_endereco(self, rua, numero, cidade):
        self.endereco = Endereco(rua, numero, cidade)

    def remover(self):
        """Remove o aluno e repassa o endereço (ele continua existindo)."""
        endereco, self.endereco = self.endereco, None
        return endereco


class Professor:
    """Existe independentemente de qualquer escola (agregação)."""

    def __init__(self, nome, disciplina):
        self.nome = nome
        self.disciplina = disciplina
        self._escolas = []

    def lecionar(self, escola):
        if escola not in self._escolas:
            self._escolas.append(escola)

    def deixar_escola(self, escola):
        if escola in self._escolas:
            self._escolas.remove(escola)

    def listar_escolas(self):
        return [e.nome for e in self._escolas]


class Sala:
    """Só faz sentido dentro de uma Escola (composição)."""

    def __init__(self, numero, capacidade):
        self.numero = numero
        self.capacidade = capacidade

    def descricao(self):
        return f"Sala {self.numero} (capacidade: {self.capacidade})"


class Escola:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self._salas = []          # composição: a escola cria suas salas
        self._professores = []    # agregação: professores já existem

    # --- composição
    def adicionar_sala(self, numero, capacidade):
        sala = Sala(numero, capacidade)   # instanciada dentro da escola
        self._salas.append(sala)
        return sala

    def listar_salas(self):
        return [s.descricao() for s in self._salas]

    def fechar(self):
        """Ao fechar a escola, as salas deixam de existir."""
        self._salas.clear()
        for professor in list(self._professores):
            professor.deixar_escola(self)
        self._professores.clear()

    # --- agregação
    def contratar_professor(self, professor):
        if professor not in self._professores:
            self._professores.append(professor)
            professor.lecionar(self)

    def listar_professores(self):
        return [p.nome for p in self._professores]


# ------------------------------------------------------------------- TESTE
if __name__ == "__main__":
    escola_a = Escola("Escola Aurora", "11.111.111/0001-11")
    escola_b = Escola("Colégio Horizonte", "22.222.222/0001-22")

    escola_a.adicionar_sala(101, 30)
    escola_a.adicionar_sala(102, 25)
    print("Salas:", escola_a.listar_salas())

    prof = Professor("Carlos Lima", "Matemática")
    escola_a.contratar_professor(prof)
    escola_b.contratar_professor(prof)
    print("Escolas do professor:", prof.listar_escolas())
    print("Professores da escola A:", escola_a.listar_professores())

    aluno = Aluno("Ana Souza", "2026001", "Rua das Flores", 45, "Parnaíba")
    print("Endereço do aluno:", aluno.endereco.formatar())
    endereco_salvo = aluno.remover()
    print("Aluno removido; endereço continua:", endereco_salvo.formatar())

    escola_a.fechar()
    print("Salas após fechar a escola A:", escola_a.listar_salas())
    print("Professor continua existindo:", prof.nome, "->", prof.listar_escolas())