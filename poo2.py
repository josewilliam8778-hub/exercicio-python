"""Trabalho Prática 02 - Sistema de Gerenciamento de uma Locadora de Veículos.

Implementação parcial em Python:
  - Herança: Cliente -> PessoaFisica / PessoaJuridica
             Veiculo -> Carro / Moto / Caminhao
  - Composição: Contrato *-- Condutor   (o contrato instancia o condutor)
  - Composição: Veiculo  *-- Manutencao (o veículo instancia suas manutenções)
  - Associação: Contrato --> Cliente e Contrato --> Veiculo (objetos recebidos)
"""
from abc import ABC, abstractmethod
from datetime import date

class Cliente(ABC):
    def __init__(self, nome, documento, telefone):
        self.nome = nome
        self.documento = documento
        self.telefone = telefone

    @abstractmethod
    def descricao(self):
        ...

    def atualizar_telefone(self, novo_telefone):
        self.telefone = novo_telefone


class PessoaFisica(Cliente):
    def descricao(self):
        return f"Pessoa Física: {self.nome} (CPF {self.documento})"


class PessoaJuridica(Cliente):
    def descricao(self):
        return f"Pessoa Jurídica: {self.nome} (CNPJ {self.documento})"



class Manutencao:
    def __init__(self, data, tipo_servico, custo):
        self.data = data
        self.tipo_servico = tipo_servico
        self.custo = custo

    def __str__(self):
        return f"{self.data:%d/%m/%Y} - {self.tipo_servico} - R$ {self.custo:.2f}"


class Veiculo(ABC):
    def __init__(self, placa, modelo, ano, valor_diaria):
        self.placa = placa
        self.modelo = modelo
        self.ano = ano
        self.valor_diaria = valor_diaria
        self.contrato_ativo = None         
        self._manutencoes = []

    def registrar_manutencao(self, data, tipo_servico, custo):
        manutencao = Manutencao(data, tipo_servico, custo)  
        self._manutencoes.append(manutencao)
        return manutencao

    def custo_total_manutencao(self):
        return sum(m.custo for m in self._manutencoes)

    def historico(self):
        return list(self._manutencoes)

    @abstractmethod
    def calcular_aluguel(self, dias):
        ...


class Carro(Veiculo):
    def __init__(self, placa, modelo, ano, valor_diaria, portas=4):
        super().__init__(placa, modelo, ano, valor_diaria)
        self.portas = portas

    def calcular_aluguel(self, dias):
        return self.valor_diaria * dias


class Moto(Veiculo):
    def __init__(self, placa, modelo, ano, valor_diaria, cilindradas=160):
        super().__init__(placa, modelo, ano, valor_diaria)
        self.cilindradas = cilindradas

    def calcular_aluguel(self, dias):
        return self.valor_diaria * dias


class Caminhao(Veiculo):
    def __init__(self, placa, modelo, ano, valor_diaria, capacidade_kg=0):
        super().__init__(placa, modelo, ano, valor_diaria)
        self.capacidade_kg = capacidade_kg

    def calcular_aluguel(self, dias):
        taxa_carga = 50.0                    # taxa fixa por dia para caminhões
        return (self.valor_diaria + taxa_carga) * dias


# ----------------------------------------------------------------- CONDUTOR
class Condutor:
    def __init__(self, nome, cnh):
        self.nome = nome
        self.cnh = cnh

    def cnh_valida(self):
        return len(str(self.cnh)) == 11

    def __str__(self):
        return f"{self.nome} (CNH {self.cnh})"


class Contrato:
    def __init__(self, cliente, veiculo, data_inicio, data_fim_prevista,
                 nome_condutor, cnh_condutor):
        if veiculo.contrato_ativo is not None:
            raise ValueError(f"O veículo {veiculo.placa} já está em um contrato ativo.")

        self.cliente = cliente
        self.veiculo = veiculo

        self.data_inicio = data_inicio
        self.data_fim_prevista = data_fim_prevista
        self.status = "ativo"
        self.valor_total = veiculo.calcular_aluguel(self.dias())

        self.condutor = Condutor(nome_condutor, cnh_condutor)

        veiculo.contrato_ativo = self

    def dias(self):
        return max((self.data_fim_prevista - self.data_inicio).days, 1)

    def finalizar(self):
        self.status = "finalizado"
        self.veiculo.contrato_ativo = None

    def cancelar(self):
        self.status = "cancelado"
        self.veiculo.contrato_ativo = None


if __name__ == "__main__":
    cliente = PessoaFisica("Maria Silva", "123.456.789-00", "(86) 99999-0000")
    empresa = PessoaJuridica("Transporte Norte Ltda", "12.345.678/0001-90", "(86) 3322-0000")
    carro = Carro("ABC-1D23", "Onix", 2023, 150.0)
    caminhao = Caminhao("XYZ-9K87", "Volvo FH", 2021, 400.0, capacidade_kg=12000)

    contrato = Contrato(cliente, carro, date(2026, 10, 10), date(2026, 10, 15),
                        "Maria Silva", "12345678901")
    print(cliente.descricao())
    print(f"Veículo: {carro.modelo} | Dias: {contrato.dias()} | Total: R$ {contrato.valor_total:.2f}")
    print("Condutor:", contrato.condutor, "| CNH válida:", contrato.condutor.cnh_valida())

    # regra: um veículo não pode ter dois contratos ativos
    try:
        Contrato(empresa, carro, date(2026, 10, 12), date(2026, 10, 14), "João", "10987654321")
    except ValueError as erro:
        print("Erro esperado:", erro)

    contrato.finalizar()
    carro.registrar_manutencao(date(2026, 10, 16), "Troca de óleo", 250.0)
    carro.registrar_manutencao(date(2026, 11, 20), "Alinhamento", 120.0)
    for m in carro.historico():
        print("Manutenção:", m)
    print(f"Custo total de manutenção: R$ {carro.custo_total_manutencao():.2f}")

    contrato2 = Contrato(empresa, caminhao, date(2026, 10, 20), date(2026, 10, 22), "João Souza", "10987654321")
    print(f"Contrato caminhão: R$ {contrato2.valor_total:.2f}")