"""Trabalho Prática 02 - Sistema de Gerenciamento de uma Locadora de Veículos.

Implementação parcial em Python:
  - Herança: Cliente -> PessoaFisica / PessoaJuridica
             Veiculo -> Carro / Moto / Caminhao
  - Composição: Contrato *-- Condutor   (o contrato instancia o condutor)
  - Composição: Veiculo  *-- Manutencao (o veículo instancia suas manutenções)
  - Associação: Contrato --> Cliente e Contrato --> Veiculo (objetos recebidos)
"""
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Optional


class Manutencao:
    def __init__(self, id_manutencao: int, data: date, tipo_servico: str, custo: float):
        self.id = id_manutencao
        self.data = data
        self.tipo_servico = tipo_servico
        self.custo = custo

    def __str__(self) -> str:
        return f"  [Manutenção #{self.id}] {self.data} | {self.tipo_servico} | R$ {self.custo:.2f}"


class Veiculo(ABC):
    def __init__(self, placa: str, modelo: str, marca: str, ano: int, valor_diaria: float):
        self.placa = placa
        self.modelo = modelo
        self.marca = marca
        self.ano = ano
        self.valor_diaria = valor_diaria
        self.disponivel = True
        self.manutencoes: List[Manutencao] = []
        self._seq_manutencao = 1

    def registrar_manutencao(self, data: date, tipo_servico: str, custo: float):
        # Cria a manutenção direto aqui dentro pra garantir que ela pertence ao veículo
        m = Manutencao(self._seq_manutencao, data, tipo_servico, custo)
        self._seq_manutencao += 1
        self.manutencoes.append(m)
        return m

    def custo_total_manutencoes(self) -> float:
        return sum(m.custo for m in self.manutencoes)

    def ver_historico(self):
        if not self.manutencoes:
            print(f"Sem manutenções para o veículo {self.placa}.")
            return
        
        print(f"Histórico de manutenções — {self.placa} ({self.modelo}):")
        for m in self.manutencoes:
            print(m)
        print(f"  TOTAL GASTO: R$ {self.custo_total_manutencoes():.2f}")

    @abstractmethod
    def exibir_info(self):
        pass

    def calcular_locacao(self, dias: int) -> float:
        return self.valor_diaria * dias


class Carro(Veiculo):
    def __init__(self, placa, modelo, marca, ano, valor_diaria, num_portas, tipo_cambio):
        super().__init__(placa, modelo, marca, ano, valor_diaria)
        self.num_portas = num_portas
        self.tipo_cambio = tipo_cambio

    def exibir_info(self):
        status = "Disponível" if self.disponivel else "Alugado"
        return f"[CARRO] {self.marca} {self.modelo} ({self.ano}) - Placa: {self.placa} | {status}"


class Moto(Veiculo):
    def __init__(self, placa, modelo, marca, ano, valor_diaria, cilindradas):
        super().__init__(placa, modelo, marca, ano, valor_diaria)
        self.cilindradas = cilindradas

    def exibir_info(self):
        status = "Disponível" if self.disponivel else "Alugado"
        return f"[MOTO] {self.marca} {self.modelo} ({self.ano}) - Placa: {self.placa} | {self.cilindradas}cc | {status}"


class Condutor:
    def __init__(self, nome: str, numero_cnh: str, categoria_cnh: str = "B", validade_cnh: date = None):
        self.nome = nome
        self.numero_cnh = numero_cnh
        self.categoria_cnh = categoria_cnh
        self.validade_cnh = validade_cnh

    def cnh_valida(self) -> bool:
        if not self.validade_cnh:
            return True
        return self.validade_cnh >= date.today()

    def __str__(self):
        return f"Condutor: {self.nome} (CNH: {self.numero_cnh})"


class Contrato:
    def __init__(self, id_contrato: int, data_inicio: date, dias: int, veiculo: Veiculo, nome_condutor: str, cnh: str, categoria: str = "B"):
        self.id = id_contrato
        self.data_inicio = data_inicio
        self.data_termino = data_inicio + timedelta(days=dias)
        self.veiculo = veiculo
        self.status = "ativo"
        
        # Instancia o condutor aqui dentro porque ele é exclusivo desse contrato
        self.condutor = Condutor(nome_condutor, cnh, categoria)
        
        self.valor_total = veiculo.calcular_locacao(dias)
        veiculo.disponivel = False  # já trava o carro

    def encerrar(self, data_real: date = None):
        if self.status != "ativo":
            print("Erro: Esse contrato já foi encerrado.")
            return

        data_real = data_real or date.today()
        self.status = "encerrado"
        self.veiculo.disponivel = True

        # TODO: conferir se a regra de multa tá certa
        if data_real > self.data_termino:
            dias_extra = (data_real - self.data_termino).days
            multa = dias_extra * self.veiculo.valor_diaria * 0.20
            self.valor_total += multa

        return self.valor_total

    def __str__(self):
        return f"Contrato #{self.id} ({self.status}) | Veículo: {self.veiculo.placa} | {self.condutor} | R$ {self.valor_total:.2f}"


if __name__ == "__main__":
    print("Testando o sistema...")

    # Testando carro e manutenções
    meu_carro = Carro("ABC-1234", "Corolla", "Toyota", 2023, 180.0, 4, "Automático")
    print(meu_carro.exibir_info())

    meu_carro.registrar_manutencao(date(2024, 1, 15), "Troca de óleo", 250.0)
    meu_carro.registrar_manutencao(date(2024, 3, 10), "Revisão", 1200.0)
    
    print()
    meu_carro.ver_historico()

    print("-" * 40)

    # Testando moto e contrato
    minha_moto = Moto("XYZ-9876", "CB 500", "Honda", 2024, 90.0, 500)
    
    contrato = Contrato(
        id_contrato=1,
        data_inicio=date(2024, 6, 1),
        dias=5,
        veiculo=minha_moto,
        nome_condutor="Carlos Silva",
        cnh="98765432100"
    )

    print(contrato)
    print(f"Moto tá disponível? {minha_moto.disponivel}")

    # Fechando o contrato
    contrato.encerrar(date(2024, 6, 8)) # devolveu com atraso
    print("\nDepois de encerrar:")
    print(contrato)
    print(f"Moto tá disponível agora? {minha_moto.disponivel}")